from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Venue, VenueSpace, Seating
from .serializers import (
	VenueSerializer,
	VenueDetailSerializer,
	VenueCreateSerializer,
	VenueSpaceSerializer,
	VenueSpaceDetailSerializer,
	VenueSpaceCreateSerializer,
	SeatingSerializer,
	SeatingCreateSerializer,
)


class VenueViewSet(viewsets.ModelViewSet):
	queryset = Venue.objects.all()
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return VenueDetailSerializer
		if self.action in ['create', 'update', 'partial_update']:
			return VenueCreateSerializer
		return VenueSerializer

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Venue.objects.all()
		if user.tenant:
			return Venue.objects.filter(tenant=user.tenant)
		return Venue.objects.none()


class VenueSpaceViewSet(viewsets.ModelViewSet):
	queryset = VenueSpace.objects.all()
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return VenueSpaceDetailSerializer
		if self.action in ['create', 'update', 'partial_update']:
			return VenueSpaceCreateSerializer
		return VenueSpaceSerializer

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return VenueSpace.objects.all()
		if user.tenant:
			return VenueSpace.objects.filter(venue__tenant=user.tenant)
		return VenueSpace.objects.none()


class SeatingViewSet(viewsets.ModelViewSet):
	queryset = Seating.objects.all()
	serializer_class = SeatingSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Seating.objects.all()
		if user.tenant:
			return Seating.objects.filter(space__venue__tenant=user.tenant)
		return Seating.objects.none()
