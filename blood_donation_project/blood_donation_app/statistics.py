# Define a dictionary to map blood types to their corresponding codes
# from .models import DonationRecord
# def total_blooddonation_of_each_type():
#     blood_type_codes_mapping = {
#         'O+': 'Opositive',
#         'O-': 'Onegative',
#         'A+': 'Apositive',
#         'A-': 'Anegative',
#         'B+': 'Bpositive',
#         'B-': 'Bnegative',
#         'AB+': 'ABpositive',
#         'AB-': 'ABnegative',
#     }

#     # Initialize blood type counts dictionary
#     blood_type_counts = {blood_type: 0 for blood_type in blood_type_codes_mapping.keys()}

#     # Iterate over DonationRecord queryset and count occurrences of each blood type
#     for donation_record in DonationRecord.objects.all():
#         donor_blood_type = donation_record.donor.donor_blood_type.blood_type
#         if donor_blood_type in blood_type_codes_mapping:
#             blood_type_counts[donor_blood_type] += 1

#     # Print or use blood_type_counts as needed
#     print(blood_type_counts)


# from django.db.models import Count
# from .models import DonationRecord

# def total_blooddonation_of_each_type():
#     # Define a dictionary to map blood types to their corresponding codes
#     blood_type_codes_mapping = {
#         'O+': 'Opositive',
#         'O-': 'Onegative',
#         'A+': 'Apositive',
#         'A-': 'Anegative',
#         'B+': 'Bpositive',
#         'B-': 'Bnegative',
#         'AB+': 'ABpositive',
#         'AB-': 'ABnegative',
#     }

#     # Query the database to count occurrences of each blood type
#     blood_type_counts = DonationRecord.objects.values('donor__donor_blood_type__blood_type').annotate(
#         count=Count('id')
#     ).order_by()

#     # Initialize blood type counts dictionary
#     blood_type_totals = {blood_type: 0 for blood_type in blood_type_codes_mapping.keys()}

#     # Update blood type counts dictionary with query results
#     for result in blood_type_counts:
#         blood_type = result['donor__donor_blood_type__blood_type']
#         if blood_type in blood_type_codes_mapping:
#             blood_type_totals[blood_type] = result['count']

#     # Print or use blood_type_totals as needed
#     print(blood_type_totals)




from django.db.models import Sum, Case, When, IntegerField, F
from .models import DonationRecord

def total_blooddonation_of_each_type():
    # Define a dictionary to map blood types to their corresponding codes
    blood_type_codes_mapping = {
        'O+': 'Opositive',
        'O-': 'Onegative',
        'A+': 'Apositive',
        'A-': 'Anegative',
        'B+': 'Bpositive',
        'B-': 'Bnegative',
        'AB+': 'ABpositive',
        'AB-': 'ABnegative',
    }

    blood_type_totals = DonationRecord.objects.aggregate(
        Opositive=Sum(Case(When(donor__donor_blood_type__blood_type='O+', then=1), default=0, output_field=IntegerField())),
        Onegative=Sum(Case(When(donor__donor_blood_type__blood_type='O-', then=1), default=0, output_field=IntegerField())),
        Apositive=Sum(Case(When(donor__donor_blood_type__blood_type='A+', then=1), default=0, output_field=IntegerField())),
        Anegative=Sum(Case(When(donor__donor_blood_type__blood_type='A-', then=1), default=0, output_field=IntegerField())),
        Bpositive=Sum(Case(When(donor__donor_blood_type__blood_type='B+', then=1), default=0, output_field=IntegerField())),
        Bnegative=Sum(Case(When(donor__donor_blood_type__blood_type='B-', then=1), default=0, output_field=IntegerField())),
        ABpositive=Sum(Case(When(donor__donor_blood_type__blood_type='AB+', then=1), default=0, output_field=IntegerField())),
        ABnegative=Sum(Case(When(donor__donor_blood_type__blood_type='AB-', then=1), default=0, output_field=IntegerField())),
    )

    # Convert the result to a dictionary
    blood_type_totals_dict = {blood_type: blood_type_totals[field] for blood_type, field in blood_type_codes_mapping.items()}

    # Print or use blood_type_totals_dict as needed
    return blood_type_totals_dict

