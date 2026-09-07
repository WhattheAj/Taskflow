from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from jobs.models import Job, JobStatus

@shared_task
def send_job_assignment_notification_task(job_id: int) -> str:
    job = Job.objects.select_related('assignee', 'creator').filter(pk=job_id).first()
    if not job or not job.assignee or not job.assignee.email:
        return f"No notification sent for job #{job_id}: missing assignee"

    subject = f"New Job Assigned: {job.title}"
    message = f"Hello {job.assignee.first_name or job.assignee.email},\n\nYou have been assigned to job '{job.title}'.\nPriority: {job.priority}\nDue Date: {job.due_date}\n\nTaskflow System"
    from_email = 'noreply@taskflow.local'
    recipient_list = [job.assignee.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
    return f"Notification sent to {job.assignee.email} for job #{job.id}"

@shared_task
def check_upcoming_deadlines_task() -> str:
    now = timezone.now()
    next_24h = now + timedelta(hours=24)
    active_statuses = [JobStatus.PENDING, JobStatus.IN_PROGRESS, JobStatus.IN_REVIEW]

    upcoming_jobs = Job.objects.select_related('assignee').filter(
        status__in=active_statuses,
        due_date__gte=now,
        due_date__lte=next_24h,
        assignee__isnull=False,
    )

    notified_count = 0
    for job in upcoming_jobs:
        if job.assignee and job.assignee.email:
            subject = f"Deadline Warning: '{job.title}' is due soon!"
            message = f"Hello {job.assignee.first_name or job.assignee.email},\n\nReminder: Your assigned job '{job.title}' is due within 24 hours on {job.due_date}.\n\nTaskflow System"
            from_email = 'noreply@taskflow.local'
            send_mail(subject, message, from_email, [job.assignee.email], fail_silently=True)
            notified_count += 1

    return f"Processed {upcoming_jobs.count()} jobs, sent {notified_count} deadline warnings."
