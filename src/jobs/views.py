from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.filters import JobFilter
from jobs.models import Category, Job, JobComment
from jobs.permissions import IsJobAssigneeOrCreatorOrManager, IsJobCreatorOrAdmin
from jobs.serializers import (
    CategorySerializer,
    JobCommentSerializer,
    JobCreateUpdateSerializer,
    JobDetailSerializer,
    JobListSerializer,
    JobStatusUpdateSerializer,
)
from users.models import UserRole

from django.core.cache import cache
from jobs.constants import CacheKeys

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'created_at')

    def list(self, request, *args, **kwargs):
        cache_key = CacheKeys.get_category_list_key()
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response

    def perform_create(self, serializer):
        serializer.save()
        cache.delete(CacheKeys.get_category_list_key())

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(CacheKeys.get_category_list_key())

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(CacheKeys.get_category_list_key())

class JobViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = JobFilter
    search_fields = ('title', 'description')
    ordering_fields = ('created_at', 'due_date', 'priority', 'status')

    def get_queryset(self):
        user = self.request.user
        queryset = Job.objects.select_related('category', 'creator', 'assignee').prefetch_related('comments__author', 'activity_logs__actor')

        if user.role in (UserRole.ADMIN, UserRole.MANAGER):
            return queryset

        return queryset.filter(creator=user) | queryset.filter(assignee=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        if self.action == 'retrieve':
            return JobDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return JobCreateUpdateSerializer
        if self.action == 'update_status':
            return JobStatusUpdateSerializer
        return JobDetailSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsJobCreatorOrAdmin()]
        if self.action == 'update_status':
            return [IsAuthenticated(), IsJobAssigneeOrCreatorOrManager()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        job = self.get_object()
        serializer = JobStatusUpdateSerializer(job, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(JobDetailSerializer(job).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        job = self.get_object()
        if request.method == 'GET':
            comments = job.comments.all()
            serializer = JobCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = JobCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(job=job, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
