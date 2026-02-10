"""
Django management command to generate attendee matching recommendations.

Usage: python manage.py generate_matches [--tenant_id=<id>] [--top_n=3]
"""

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from accounts.models import User
from networking.models import NetworkProfile, RecommendedConnection
from networking.utils import batch_calculate_matches


class Command(BaseCommand):
    help = 'Generate intelligent attendee matching recommendations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tenant_id',
            type=int,
            help='Tenant ID to generate matches for (optional)',
        )
        parser.add_argument(
            '--top_n',
            type=int,
            default=3,
            help='Number of top matches per user (default: 3)',
        )

    def handle(self, *args, **options):
        tenant_id = options.get('tenant_id')
        top_n = options.get('top_n', 3)

        # Get all users
        user_qs = User.objects.all()
        if tenant_id:
            user_qs = user_qs.filter(tenant_id=tenant_id)

        if not user_qs.exists():
            raise CommandError('No users found')

        # Get network profiles
        profiles_qs = NetworkProfile.objects.filter(
            user__in=user_qs,
            show_in_discovery=True
        )

        if not profiles_qs.exists():
            raise CommandError('No network profiles found')

        # Prepare data for batch matching
        user_profiles = []
        profile_map = {}
        
        for profile in profiles_qs:
            user_profiles.append({
                'id': profile.user.id,
                'interests': profile.interests or [],
                'expertise': profile.expertise or [],
                'department': profile.user.username or '',
            })
            profile_map[profile.user.id] = profile

        # Calculate batch matches
        try:
            matches_dict = batch_calculate_matches(user_profiles, top_n, include_reason=True)
        except Exception as e:
            raise CommandError(f'Failed to calculate matches: {str(e)}')

        # Save recommendations to database
        created_count = 0
        for user_id, matches in matches_dict.items():
            for match in matches:
                try:
                    rec, created = RecommendedConnection.objects.update_or_create(
                        user_id=user_id,
                        recommended_user_id=match['user_id'],
                        defaults={
                            'match_score': match['match_score'],
                            'reason': match.get('reason', 'Matched interests'),
                        }
                    )
                    if created:
                        created_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Failed to save recommendation for user {user_id}: {str(e)}'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Generated recommendations for {len(matches_dict)} users'
            )
        )
        self.stdout.write(f'  Total recommendations created: {created_count}')
        self.stdout.write(f'  Top N matches per user: {top_n}')
