from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from jobs.models import Job, JobPriority, JobStatus
from jobs.tasks import send_job_assignment_notification_task
from users.models import UserRole

User = get_user_model()

class CeleryTasksTestCase(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(
            email='creator_task@example.com',
            password='password123',
            role=UserRole.MANAGER,
        )
        self.assignee = User.objects.create_user(
            email='assignee_task@example.com',
            password='password123',
            first_name='Assignee',
            role=UserRole.MEMBER,
        )
        self.job = Job.objects.create(
            title='Celery Async Task',
            description='Test Celery notification delivery',
            priority=JobPriority.HIGH,
            status=JobStatus.PENDING,
            creator=self.creator,
            assignee=self.assignee,
        )

    def test_send_job_assignment_notification_task(self):
        result = send_job_assignment_notification_task(self.job.id)
        self.assertIn('Notification sent', result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Celery Async Task', mail.outbox[0].subject)
