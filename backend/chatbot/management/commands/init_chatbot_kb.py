"""
Django management command to initialize and rebuild the chatbot knowledge base.

Usage: python manage.py init_chatbot_kb [--tenant_id=<id>] [--rebuild]
"""

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from chatbot.models import ChatbotKnowledgeBase
from chatbot.utils import initialize_knowledge_base


class Command(BaseCommand):
    help = 'Initialize or rebuild the chatbot knowledge base vector database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tenant_id',
            type=int,
            help='Tenant ID to initialize KB for (optional)',
        )
        parser.add_argument(
            '--rebuild',
            action='store_true',
            help='Rebuild the knowledge base',
        )

    def handle(self, *args, **options):
        tenant_id = options.get('tenant_id')
        rebuild = options.get('rebuild', False)

        # Get knowledge base documents
        qs = ChatbotKnowledgeBase.objects.filter(is_published=True)
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)

        if not qs.exists():
            raise CommandError('No published knowledge base documents found')

        # Build documents
        documents = [
            f"Q: {doc.title}\nA: {doc.content}\nCategory: {doc.category}"
            for doc in qs
        ]

        try:
            # Initialize knowledge base
            initialize_knowledge_base(documents, tenant_id)
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Successfully initialized knowledge base with {len(documents)} documents'
                )
            )
            if tenant_id:
                self.stdout.write(f'  Tenant ID: {tenant_id}')
        except Exception as e:
            raise CommandError(f'Failed to initialize knowledge base: {str(e)}')
