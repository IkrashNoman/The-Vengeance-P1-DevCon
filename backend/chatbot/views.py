import os
import uuid
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone

from .models import ChatbotKnowledgeBase, ChatbotConversation, ChatbotMessage
from .serializers import (
	ChatbotKnowledgeBaseSerializer,
	ChatbotConversationSerializer,
)
from .services import get_chatbot_service, ChatbotDataLoader

logger = logging.getLogger(__name__)


class ChatbotKnowledgeBaseViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for managing chatbot knowledge base documents.
	Endpoint: /api/chatbot/knowledge-base/
	"""
	queryset = ChatbotKnowledgeBase.objects.all()
	serializer_class = ChatbotKnowledgeBaseSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return ChatbotKnowledgeBase.objects.all()
		if user.tenant:
			return ChatbotKnowledgeBase.objects.filter(tenant=user.tenant)
		return ChatbotKnowledgeBase.objects.none()

	@action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
	def rebuild_knowledge_base(self, request):
		"""
		Rebuild the Chroma vector database from current knowledge base documents.
		POST /api/chatbot/knowledge-base/rebuild_knowledge_base/
		"""
		user = request.user
		
		# Get knowledge base for user's tenant
		if user.is_super_admin():
			documents_qs = ChatbotKnowledgeBase.objects.filter(is_published=True)
		else:
			documents_qs = ChatbotKnowledgeBase.objects.filter(
				tenant=user.tenant,
				is_published=True
			)
		
		if not documents_qs.exists():
			# Load default knowledge base if none exists
			docs = ChatbotDataLoader.get_default_knowledge_base()
			logger.info(f"No published documents found. Loading {len(docs)} default documents.")
		else:
			# Build documents from knowledge base
			docs = [
				f"Q: {doc.title}\nA: {doc.content}\nCategory: {doc.category}"
				for doc in documents_qs
			]
		
		try:
			# Get chatbot service and build knowledge base
			service = get_chatbot_service()
			db_path = f"./chroma_db_{user.tenant.id}" if user.tenant else "./chroma_db_default"
			success = service.build_knowledge_base(docs, db_path)
			
			if success:
				return Response({
					'message': f'Knowledge base rebuilt successfully with {len(docs)} documents',
					'document_count': len(docs),
					'db_path': db_path
				}, status=status.HTTP_200_OK)
			else:
				return Response(
					{'error': 'Failed to rebuild knowledge base. Check logs for details.'},
					status=status.HTTP_500_INTERNAL_SERVER_ERROR
				)
		except Exception as e:
			logger.error(f"Failed to rebuild knowledge base: {str(e)}")
			return Response(
				{'error': f'Failed to rebuild knowledge base: {str(e)}'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)


class ChatbotConversationViewSet(viewsets.ModelViewSet):
	"""
	ViewSet for chatbot conversations and RAG-powered responses.
	Endpoint: /api/chatbot/conversations/
	"""
	queryset = ChatbotConversation.objects.all()
	serializer_class = ChatbotConversationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return ChatbotConversation.objects.all()
		return ChatbotConversation.objects.filter(user=user)

	def create(self, request, *args, **kwargs):
		"""
		Create a new conversation session.
		POST /api/chatbot/conversations/ with {"message": "user question"}
		"""
		user = request.user
		message = request.data.get('message', '')
		olympiad_id = request.data.get('olympiad_id')
		
		if not message:
			return Response(
				{'error': 'Message is required'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		# Create conversation session
		session_id = str(uuid.uuid4())
		conversation = ChatbotConversation.objects.create(
			user=user,
			olympiad_id=olympiad_id,
			session_id=session_id,
			message_count=1,
			resolution_status='open'
		)
		
		# Get chatbot response
		try:
			response_text = self._get_rag_response(user, message, olympiad_id)
			
			# Update conversation stats
			conversation.message_count = 1
			conversation.updated_at = timezone.now()
			conversation.save()
			
			return Response({
				'session_id': session_id,
				'user_message': message,
				'bot_response': response_text,
				'created_at': conversation.created_at
			}, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response(
				{'error': f'Failed to get response: {str(e)}'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	@action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
	def send_message(self, request, pk=None):
		"""
		Send a message in an existing conversation.
		POST /api/chatbot/conversations/{id}/send_message/ with {"message": "user question"}
		"""
		conversation = self.get_object()
		user = request.user
		message = request.data.get('message', '')
		
		# Verify user owns conversation
		if conversation.user != user and not user.is_super_admin():
			return Response(
				{'error': 'Permission denied'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		if not message:
			return Response(
				{'error': 'Message is required'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		try:
			# Get RAG response
			response_text = self._get_rag_response(user, message, conversation.olympiad_id)
			
			# Update conversation
			conversation.message_count += 1
			conversation.updated_at = timezone.now()
			conversation.save()
			
			return Response({
				'session_id': conversation.session_id,
				'user_message': message,
				'bot_response': response_text,
				'message_count': conversation.message_count
			}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response(
				{'error': f'Failed to get response: {str(e)}'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	def _get_rag_response(self, user, user_message, olympiad_id=None):
		"""
		Get response using RAG with Groq LLM and Chroma vector store.
		Uses the ChatbotService for RAG-powered response generation.
		"""
		try:
			# Get chatbot service
			service = get_chatbot_service()
			
			# Determine database path
			db_path = f"./chroma_db_{user.tenant.id}" if user.tenant else "./chroma_db_default"
			
			# Try to load existing knowledge base
			service.load_knowledge_base(db_path)
			
			# If no knowledge base exists, build from document base or use defaults
			if service.vectordb is None:
				if user.is_super_admin():
					documents_qs = ChatbotKnowledgeBase.objects.filter(
						is_published=True,
						olympiad_id=olympiad_id
					) if olympiad_id else ChatbotKnowledgeBase.objects.filter(is_published=True)
				else:
					documents_qs = ChatbotKnowledgeBase.objects.filter(
						tenant=user.tenant,
						is_published=True,
						olympiad_id=olympiad_id
					) if olympiad_id else ChatbotKnowledgeBase.objects.filter(
						tenant=user.tenant,
						is_published=True
					)
				
				if documents_qs.exists():
					# Build from custom documents
					docs = [
						f"Q: {doc.title}\nA: {doc.content}\nCategory: {doc.category}"
						for doc in documents_qs
					]
				else:
					# Use default knowledge base
					docs = ChatbotDataLoader.get_default_knowledge_base()
				
				# Build knowledge base
				service.build_knowledge_base(docs, db_path)
			
			# Get response using the service
			response, doc_ids = service.get_response(user_message)
			
			# Save message to database
			try:
				# Get or find the conversation session
				conversation = ChatbotConversation.objects.filter(
					user=user,
					resolution_status='open'
				).first()
				
				if conversation:
					# Save bot response
					ChatbotMessage.objects.create(
						conversation=conversation,
						message_type='bot',
						content=response,
						retrieved_documents=doc_ids
					)
				
			except Exception as e:
				logger.error(f"Failed to save chatbot message: {str(e)}")
			
			return response
			
		except Exception as e:
			logger.error(f"Error generating RAG response: {str(e)}")
			return f"Error generating response: {str(e)}"
