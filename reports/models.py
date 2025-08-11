from django.db import models
from django.conf import settings


class BaseReport(models.Model):
    REPORT_TYPES = (
        ('MEMBERSHIP', 'Membership'),
        ('ATTENDANCE', 'Attendance'),
        ('FEEDBACK', 'Feedback'),
    )

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_reports"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MembershipReport(BaseReport):
    total_members = models.PositiveIntegerField()
    active_members = models.PositiveIntegerField()
    inactive_members = models.PositiveIntegerField()
    related_name = "membership_reports"

    def __str__(self):
        return f"Membership Report: {self.title}"


class AttendanceReport(BaseReport):
    total_sessions = models.PositiveIntegerField()
    total_attendees = models.PositiveIntegerField()
    average_attendance = models.FloatField()
    related_name = "attendance_reports"

    def __str__(self):
        return f"Attendance Report: {self.title}"


class FeedbackReport(BaseReport):
    total_feedback = models.PositiveIntegerField()
    average_rating = models.FloatField()
    positive_feedback_count = models.PositiveIntegerField()
    negative_feedback_count = models.PositiveIntegerField()
    related_name = "feedback_reports"

    def __str__(self):
        return f"Feedback Report: {self.title}"
