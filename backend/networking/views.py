from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
import numpy as np
import logging

from .models import NetworkProfile, Connection, RecommendedConnection
from .serializers import (
	NetworkProfileSerializer,
	ConnectionSerializer,
	RecommendedConnectionSerializer,
)
from .services import get_matching_service, ConnectionRecommendationService
from accounts.models import User

logger = logging.getLogger(__name__)

# Semantic matching imports
try:
	from sentence_transformers import SentenceTransformer
	from sklearn.metrics.pairwise import cosine_similarity
	SEMANTIC_MATCHING_AVAILABLE = True
except ImportError:
	SEMANTIC_MATCHING_AVAILABLE = False


class NetworkProfileViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for managing user networking profiles.
	Endpoint: /api/networking/profiles/
	"""
	queryset = NetworkProfile.objects.all()
	serializer_class = NetworkProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return NetworkProfile.objects.all()
		if user.tenant:
			return NetworkProfile.objects.filter(user__tenant=user.tenant)
		return NetworkProfile.objects.none()

	@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
	def my_profile(self, request):
		"""
		Get current user's network profile.
		GET /api/networking/profiles/my_profile/
		"""
		user = request.user
		profile, created = NetworkProfile.objects.get_or_create(user=user)
		serializer = self.get_serializer(profile)
		return Response(serializer.data)

	@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
	def discover(self, request):
		"""
		Discover other users for networking based on visibility preferences.
		GET /api/networking/profiles/discover/?limit=10
		"""
		user = request.user
		limit = int(request.query_params.get('limit', 10))
		
		# Get all discoverable profiles except user's own
		profiles = NetworkProfile.objects.filter(
			show_in_discovery=True,
			user__tenant=user.tenant if not user.is_super_admin() else Q()
		).exclude(user=user)[:limit]
		
		serializer = self.get_serializer(profiles, many=True)
		return Response(serializer.data)

	@action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
	def find_matches(self, request, pk=None):
		"""
		Find semantic matches for a user based on interests and role.
		POST /api/networking/profiles/{id}/find_matches/?top_n=3
		"""
		target_profile = self.get_object()
		user = request.user
		
		# Verify permission
		if target_profile.user != user and not user.is_super_admin():
			return Response(
				{'error': 'Permission denied'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		if not SEMANTIC_MATCHING_AVAILABLE:
			return Response(
				{'error': 'Semantic matching not available. Please install required dependencies.'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
		
		top_n = int(request.query_params.get('top_n', 3))
		
		try:
			matching_service = get_matching_service()
			matches = matching_service.find_top_matches(target_profile, top_n)
			return Response({
				'user_id': target_profile.user.id,
				'matches': matches
			}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response(
				{'error': f'Failed to find matches: {str(e)}'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	def _find_semantic_matches(self, target_profile, top_n=3):
		"""
		Find semantic matches using the matching service.
		Delegates to NetworkMatchingService for actual matching logic.
		"""
		matching_service = get_matching_service()
		return matching_service.find_top_matches(target_profile, top_n)


class ConnectionViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for managing networking connections between users.
	Endpoint: /api/networking/connections/
	"""
	queryset = Connection.objects.all()
	serializer_class = ConnectionSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Connection.objects.all()
		return Connection.objects.filter(Q(user_from=user) | Q(user_to=user))

	def create(self, request, *args, **kwargs):
		"""
		Create a new connection request.
		POST /api/networking/connections/ with {"user_to": id, "message": "optional message"}
		"""
		user = request.user
		user_to_id = request.data.get('user_to')
		message = request.data.get('message', '')
		
		if not user_to_id:
			return Response(
				{'error': 'user_to is required'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		# Check if connection already exists
		existing = Connection.objects.filter(
			user_from=user,
			user_to_id=user_to_id
		).first()
		
		if existing:
			return Response(
				{'error': 'Connection already exists'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		connection = Connection.objects.create(
			user_from=user,
			user_to_id=user_to_id,
			message=message,
			status='pending'
		)
		
		serializer = self.get_serializer(connection)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
	def accept(self, request, pk=None):
		"""
		Accept a connection request.
		POST /api/networking/connections/{id}/accept/
		"""
		connection = self.get_object()
		user = request.user
		
		# Only recipient can accept
		if connection.user_to != user:
			return Response(
				{'error': 'Permission denied'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		connection.status = 'connected'
		connection.connected_at = timezone.now()
		connection.save()
		
		serializer = self.get_serializer(connection)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
	def reject(self, request, pk=None):
		"""
		Reject a connection request.
		POST /api/networking/connections/{id}/reject/
		"""
		connection = self.get_object()
		user = request.user
		
		# Only recipient or sender can reject
		if connection.user_to != user and connection.user_from != user:
			return Response(
				{'error': 'Permission denied'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		connection.delete()
		return Response(
			{'message': 'Connection rejected'},
			status=status.HTTP_204_NO_CONTENT
		)


class RecommendedConnectionViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for AI-recommended connections based on matching algorithms.
	Endpoint: /api/networking/recommendations/
	"""
	queryset = RecommendedConnection.objects.all()
	serializer_class = RecommendedConnectionSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return RecommendedConnection.objects.all()
		return RecommendedConnection.objects.filter(user=user)

	@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
	def generate_recommendations(self, request):
		"""
		Generate intelligent recommendations for a user.
		POST /api/networking/recommendations/generate_recommendations/
		"""
		user = request.user
		limit = int(request.query_params.get('limit', 5))
		
		if not SEMANTIC_MATCHING_AVAILABLE:
			return Response(
				{'error': 'Semantic matching not available'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
		
		try:
			# Get or create user's profile
			user_profile, _ = NetworkProfile.objects.get_or_create(user=user)
			
			# Use matching service to find recommendations
			matching_service = get_matching_service()
			matches = matching_service.find_top_matches(user_profile, top_n=limit)
			
			# Create recommendation records
			recommendations = []
			for match in matches:
				try:
					recommended_user = User.objects.get(id=match['user_id'])
					rec = ConnectionRecommendationService.create_recommendation(
						user=user,
						recommended_user=recommended_user,
						match_score=match['match_score'],
						reason=match['reason']
					)
					recommendations.append(rec)
				except Exception as e:
					logger.error(f"Failed to create recommendation: {str(e)}")
					continue
			
			serializer = self.get_serializer(recommendations, many=True)
			return Response({
				'message': f'Generated {len(recommendations)} recommendations',
				'recommendations': serializer.data
			}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response(
				{'error': f'Failed to generate recommendations: {str(e)}'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	@action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
	def accept_recommendation(self, request, pk=None):
		"""
		Accept a recommendation and create a connection request.
		POST /api/networking/recommendations/{id}/accept_recommendation/
		"""
		recommendation = self.get_object()
		user = request.user
		
		if recommendation.user != user:
			return Response(
				{'error': 'Permission denied'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		# Create connection
		connection, created = Connection.objects.get_or_create(
			user_from=user,
			user_to=recommendation.recommended_user,
			defaults={'status': 'pending'}
		)
		
		recommendation.delete()
		
		return Response({
			'message': 'Connection request sent',
			'connection_id': connection.id
		}, status=status.HTTP_200_OK)
