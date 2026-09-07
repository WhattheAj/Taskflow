from django.db import transaction
from jobs.exceptions import InvalidStateTransitionError
from jobs.models import JobActivityLog, JobStatus

class JobStateMachine:
    ALLOWED_TRANSITIONS = {
        JobStatus.PENDING: {
            JobStatus.IN_PROGRESS,
            JobStatus.CANCELLED,
        },
        JobStatus.IN_PROGRESS: {
            JobStatus.IN_REVIEW,
            JobStatus.COMPLETED,
            JobStatus.PENDING,
            JobStatus.CANCELLED,
        },
        JobStatus.IN_REVIEW: {
            JobStatus.COMPLETED,
            JobStatus.IN_PROGRESS,
            JobStatus.CANCELLED,
        },
        JobStatus.COMPLETED: {
            JobStatus.IN_PROGRESS,
        },
        JobStatus.CANCELLED: {
            JobStatus.PENDING,
        },
    }

    @classmethod
    def can_transition(cls, old_status: str, new_status: str) -> bool:
        if old_status == new_status:
            return True
        allowed_next = cls.ALLOWED_TRANSITIONS.get(old_status, set())
        return new_status in allowed_next

    @classmethod
    def validate_transition(cls, old_status: str, new_status: str) -> None:
        if not cls.can_transition(old_status, new_status):
            raise InvalidStateTransitionError(old_status, new_status)

    @classmethod
    def transition_job(cls, job, new_status: str, actor=None, action_note: str = '') -> object:
        if job.status == new_status:
            return job

        cls.validate_transition(job.status, new_status)

        with transaction.atomic():
            old_status = job.status
            job.status = new_status
            job.save(update_fields=['status', 'updated_at'])

            action_text = action_note if action_note else f"Status changed from {old_status} to {new_status}"

            JobActivityLog.objects.create(
                job=job,
                actor=actor,
                action=action_text,
                old_status=old_status,
                new_status=new_status,
            )

        return job
