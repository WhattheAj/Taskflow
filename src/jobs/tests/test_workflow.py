from django.test import TestCase
from django.contrib.auth import get_user_model
from jobs.exceptions import InvalidStateTransitionError
from jobs.models import Job, JobActivityLog, JobStatus
from jobs.services.state_machine import JobStateMachine

User = get_user_model()

class JobWorkflowTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='creator@example.com',
            password='password123',
        )
        self.job = Job.objects.create(
            title='Test Task',
            description='Testing workflow transitions',
            creator=self.user,
            status=JobStatus.PENDING,
        )

    def test_valid_status_transition_flow(self):
        JobStateMachine.transition_job(self.job, JobStatus.IN_PROGRESS, actor=self.user)
        self.assertEqual(self.job.status, JobStatus.IN_PROGRESS)

        JobStateMachine.transition_job(self.job, JobStatus.IN_REVIEW, actor=self.user)
        self.assertEqual(self.job.status, JobStatus.IN_REVIEW)

        JobStateMachine.transition_job(self.job, JobStatus.COMPLETED, actor=self.user)
        self.assertEqual(self.job.status, JobStatus.COMPLETED)

        self.assertEqual(JobActivityLog.objects.filter(job=self.job).count(), 3)

    def test_invalid_status_transition_raises_error(self):
        with self.assertRaises(InvalidStateTransitionError):
            JobStateMachine.transition_job(self.job, JobStatus.COMPLETED, actor=self.user)

    def test_direct_model_save_validates_transition(self):
        self.job.status = JobStatus.COMPLETED
        with self.assertRaises(InvalidStateTransitionError):
            self.job.save()

    def test_cancelled_job_reopening(self):
        JobStateMachine.transition_job(self.job, JobStatus.CANCELLED, actor=self.user)
        self.assertEqual(self.job.status, JobStatus.CANCELLED)

        JobStateMachine.transition_job(self.job, JobStatus.PENDING, actor=self.user)
        self.assertEqual(self.job.status, JobStatus.PENDING)
