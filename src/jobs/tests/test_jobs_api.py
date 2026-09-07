from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from jobs.models import Category, Job, JobPriority, JobStatus
from users.models import UserRole

User = get_user_model()

class JobsAPITestCase(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            email='manager@example.com',
            password='password123',
            role=UserRole.MANAGER,
        )
        self.member = User.objects.create_user(
            email='member@example.com',
            password='password123',
            role=UserRole.MEMBER,
        )
        self.category = Category.objects.create(name='Backend Development')
        self.job = Job.objects.create(
            title='Implement Authentication',
            description='Setup JWT authentication',
            category=self.category,
            priority=JobPriority.HIGH,
            status=JobStatus.PENDING,
            creator=self.manager,
            assignee=self.member,
        )

    def test_list_jobs_authenticated(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('job-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_job(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('job-list')
        data = {
            'title': 'Setup Celery',
            'description': 'Configure Celery and Redis',
            'priority': JobPriority.MEDIUM,
            'category': self.category.id,
            'assignee': self.member.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 2)

    def test_update_job_status_action(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('job-update-status', kwargs={'pk': self.job.pk})
        data = {
            'status': JobStatus.IN_PROGRESS,
            'action_note': 'Started working on auth task',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, JobStatus.IN_PROGRESS)

    def test_add_comment_action(self):
        self.client.force_authenticate(user=self.member)
        url = reverse('job-comments', kwargs={'pk': self.job.pk})
        data = {'content': 'Working on it right now.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.job.comments.count(), 1)

    def test_filter_jobs_by_status(self):
        self.client.force_authenticate(user=self.manager)
        url = reverse('job-list') + '?status=PENDING'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
