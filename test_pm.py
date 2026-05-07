import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ptr_request_system.settings")
django.setup()
import datetime, calendar, re
from ptr_app.models import PTRRequest, DesignerEntry, ReceivingEntry, PreventM
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

base_qs = PTRRequest.objects.filter(status=7).order_by('-pk')
for ptr in base_qs:
    de = DesignerEntry.objects.filter(ptr=ptr).first()
    rcv = ReceivingEntry.objects.filter(ptr=ptr).first()
    if not de or not rcv or not rcv.rcvdate: continue
    freq = de.PMFrequency or 0
    if freq <= 0: continue
    tl_str = de.toollife or ""
    m = re.search(r'\d+', str(tl_str))
    toollife_years = int(m.group()) if m else 0
    if toollife_years <= 0: continue
    max_inspections = toollife_years * freq
    interval_months = 12 // freq
    rcv_date_only = rcv.rcvdate.date() if isinstance(rcv.rcvdate, datetime.datetime) else rcv.rcvdate
    print(f"PTR-{ptr.pk} rcv={rcv_date_only} freq={freq} tl={toollife_years}")
    
    for i in range(1, max_inspections + 1):
        target_date = add_months(rcv_date_only, interval_months * i)
        if not PreventM.objects.filter(ptr=ptr, pmdate=target_date).exists() and not PreventM.objects.filter(ptr=ptr, actualdate__isnull=False, pmdate=target_date).exists():
            print(f"  first upcoming_date={target_date}")
            break
