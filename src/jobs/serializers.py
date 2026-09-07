from rest_framework import serializers
from jobs.models import Category, Job, JobActivityLog, JobComment, JobPriority, JobStatus
from jobs.services.state_machine import JobStateMachine
from users.serializers import UserProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class JobCommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = JobComment
        fields = ('id', 'job', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'job', 'author', 'created_at', 'updated_at')

class JobActivityLogSerializer(serializers.ModelSerializer):
    actor = UserProfileSerializer(read_only=True)

    class Meta:
        model = JobActivityLog
        fields = ('id', 'job', 'actor', 'action', 'old_status', 'new_status', 'created_at')
        read_only_fields = ('id', 'job', 'actor', 'action', 'old_status', 'new_status', 'created_at')

class JobListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserProfileSerializer(read_only=True)
    assignee = UserProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'priority',
            'status',
            'category',
            'creator',
            'assignee',
            'due_date',
            'created_at',
            'updated_at',
        )

class JobDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserProfileSerializer(read_only=True)
    assignee = UserProfileSerializer(read_only=True)
    comments = JobCommentSerializer(many=True, read_only=True)
    activity_logs = JobActivityLogSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'description',
            'priority',
            'status',
            'category',
            'creator',
            'assignee',
            'due_date',
            'comments',
            'activity_logs',
            'created_at',
            'updated_at',
        )

class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'description',
            'category',
            'priority',
            'status',
            'assignee',
            'due_date',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class JobStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=JobStatus.choices)
    action_note = serializers.CharField(required=False, allow_blank=True, default='')

    def update(self, instance, validated_data):
        new_status = validated_data['status']
        action_note = validated_data.get('action_note', '')
        actor = self.context['request'].user
        return JobStateMachine.transition_job(
            job=instance,
            new_status=new_status,
            actor=actor,
            action_note=action_note,
        )
