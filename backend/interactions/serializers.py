from rest_framework import serializers
from .models import Poll, PollResponse, QnA, QnAUpvote, SessionNote, Feedback


class PollSerializer(serializers.ModelSerializer):
    """Serializer for Poll model."""

    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    session_name = serializers.CharField(source='event_session.name', read_only=True, allow_null=True)
    response_count = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = [
            'id',
            'event_session',
            'session_name',
            'created_by',
            'created_by_name',
            'question',
            'poll_type',
            'options',
            'is_active',
            'results_visible',
            'response_count',
            'created_at',
            'closed_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_response_count(self, obj):
        return obj.responses.count()


class PollResponseSerializer(serializers.ModelSerializer):
    """Serializer for PollResponse model."""

    poll_question = serializers.CharField(source='poll.question', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = PollResponse
        fields = [
            'id',
            'poll',
            'poll_question',
            'user',
            'user_email',
            'selected_option',
            'text_response',
            'rating',
            'responded_at',
        ]
        read_only_fields = ['id', 'responded_at']


class QnASerializer(serializers.ModelSerializer):
    """Serializer for QnA model."""

    asked_by_name = serializers.CharField(source='asked_by.get_full_name', read_only=True)
    answered_by_name = serializers.CharField(source='answered_by.get_full_name', read_only=True, allow_null=True)
    session_name = serializers.CharField(source='event_session.name', read_only=True, allow_null=True)

    class Meta:
        model = QnA
        fields = [
            'id',
            'event_session',
            'session_name',
            'asked_by',
            'asked_by_name',
            'question',
            'answer',
            'answered_by',
            'answered_by_name',
            'upvotes',
            'status',
            'is_featured',
            'asked_at',
            'answered_at',
            'approved_at',
        ]
        read_only_fields = ['id', 'asked_at']


class QnAUpvoteSerializer(serializers.ModelSerializer):
    """Serializer for QnAUpvote model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    qna_question = serializers.CharField(source='qna.question', read_only=True)

    class Meta:
        model = QnAUpvote
        fields = [
            'id',
            'qna',
            'qna_question',
            'user',
            'user_email',
            'upvoted_at',
        ]
        read_only_fields = ['id', 'upvoted_at']


class SessionNoteSerializer(serializers.ModelSerializer):
    """Serializer for SessionNote model."""

    session_name = serializers.CharField(source='event_session.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = SessionNote
        fields = [
            'id',
            'event_session',
            'session_name',
            'user',
            'user_email',
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Feedback model."""

    given_by_name = serializers.CharField(source='given_by.get_full_name', read_only=True)
    given_by_email = serializers.CharField(source='given_by.email', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True, allow_null=True)
    session_name = serializers.CharField(source='session.name', read_only=True, allow_null=True)

    class Meta:
        model = Feedback
        fields = [
            'id',
            'feedback_type',
            'event',
            'event_name',
            'session',
            'session_name',
            'given_by',
            'given_by_name',
            'given_by_email',
            'overall_rating',
            'content_rating',
            'organization_rating',
            'venue_rating',
            'comments',
            'suggestions',
            'given_at',
        ]
        read_only_fields = ['id', 'given_at']


class PollCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating polls."""

    class Meta:
        model = Poll
        fields = [
            'event_session',
            'created_by',
            'question',
            'poll_type',
            'options',
        ]


class QnACreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Q&A."""

    class Meta:
        model = QnA
        fields = [
            'event_session',
            'asked_by',
            'question',
        ]


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating feedback."""

    class Meta:
        model = Feedback
        fields = [
            'feedback_type',
            'event',
            'session',
            'given_by',
            'overall_rating',
            'content_rating',
            'organization_rating',
            'venue_rating',
            'comments',
            'suggestions',
        ]
