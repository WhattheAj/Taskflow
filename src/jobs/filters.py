import django_filters
from django.db.models import Q
from jobs.models import Category, Job, JobPriority, JobStatus

class JobFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=JobStatus.choices)
    priority = django_filters.ChoiceFilter(choices=JobPriority.choices)
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    assignee = django_filters.NumberFilter(field_name='assignee_id')
    creator = django_filters.NumberFilter(field_name='creator_id')
    due_date_gte = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_date_lte = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Job
        fields = ['status', 'priority', 'category', 'assignee', 'creator', 'due_date_gte', 'due_date_lte', 'search']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
