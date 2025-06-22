from django.contrib import admin
from django.apps import apps
from django.urls import path
from django.template.response import TemplateResponse

class CustomAdminSite(admin.AdminSite):
    site_header = "VetClinic Management"
    site_title = "VetClinic Admin"
    index_title = "Welcome to VetClinic Administration"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.custom_index), name='index'),
        ]
        return custom_urls + urls[1:]

    def custom_index(self, request):
        import json
        from datetime import datetime, timedelta
        from django.db.models import Count, Sum
        from django.utils import timezone
        import calendar

        # Get your models
        Appointment = apps.get_model('vetclinic', 'Appointment')
        Pet = apps.get_model('vetclinic', 'Pet')

        # Basic model stats
        stats = []
        for model in apps.get_models():
            try:
                stats.append({
                    "name": model._meta.verbose_name_plural.title(),
                    "count": model.objects.count()
                })
            except Exception:
                pass

        # Generate months for last 6 months
        end_date = timezone.now()
        start_date = end_date - timedelta(days=180)
        months = []
        appointments_by_month = []
        revenue_by_month = []

        # Get first day of start_date's month - fixed timezone handling
        current = timezone.make_aware(datetime(start_date.year, start_date.month, 1))

        # Generate data for each month
        while current <= end_date:
            month_name = calendar.month_name[current.month][:3] + " " + str(current.year)
            months.append(month_name)

            # Calculate next month properly
            if current.month == 12:
                next_month = timezone.make_aware(datetime(current.year+1, 1, 1))
            else:
                next_month = timezone.make_aware(datetime(current.year, current.month+1, 1))

            # Count appointments for this month
            count = Appointment.objects.filter(
                date__gte=current,
                date__lt=next_month
            ).count()
            appointments_by_month.append(count)

            # Calculate revenue
            try:
                revenue = Appointment.objects.filter(
                    date__gte=current,
                    date__lt=next_month
                ).aggregate(total=Sum('cost'))['total'] or 0
                revenue_by_month.append(float(revenue))
            except:
                revenue_by_month.append(0)

            current = next_month

        # Get animal type distribution
        animal_types = []
        animal_type_counts = []

        for species, count in Pet.objects.values('species').annotate(count=Count('id')).order_by('-count'):
            animal_types.append(species)
            animal_type_counts.append(count)

        # Get appointment status distribution
        status_data = Appointment.objects.values('status').annotate(count=Count('id')).order_by('-count')
        status_labels = [item['status'] for item in status_data]
        status_counts = [item['count'] for item in status_data]

        context = dict(
            self.each_context(request),
            stats=stats,
            months=json.dumps(months),
            appointments_by_month=json.dumps(appointments_by_month),
            revenue_by_month=json.dumps(revenue_by_month),
            animal_types=json.dumps(animal_types),
            animal_type_counts=json.dumps(animal_type_counts),
            status_labels=json.dumps(status_labels),
            status_counts=json.dumps(status_counts),
        )
        return TemplateResponse(request, "admin/custom_index.html", context)

custom_admin_site = CustomAdminSite(name='custom_admin')