import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ptr_request_system.settings")
django.setup()

from ptr_app.models import PTRRequest

print("Unique Statuses in PTRRequest:")
statuses = PTRRequest.objects.values_list('status', flat=True).distinct().order_by('status')
print(list(statuses))
