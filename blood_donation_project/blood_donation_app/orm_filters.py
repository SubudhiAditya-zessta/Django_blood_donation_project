from django.db.models import Q
from .models import DonationRecord
from datetime import datetime

def filter_donations_by_criteria(blood_type, start_date, end_date):
    date_range_filter = Q(donation_date__range=(start_date, end_date))
    blood_type_filter = Q(donor__donor_blood_type__blood_type=blood_type)
    query = DonationRecord.objects.filter(date_range_filter & blood_type_filter)
    return query