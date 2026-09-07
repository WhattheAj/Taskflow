from celery import shared_task
from django.core.mail import send_mail
from jobs.models import Job

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
