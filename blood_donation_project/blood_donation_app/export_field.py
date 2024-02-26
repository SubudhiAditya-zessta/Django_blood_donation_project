from import_export import fields
from datetime import datetime, timedelta
from .models import DonationRecord

class DonationFrequencyField(fields.Field):
    # def get_last_donation_date(self, donor):
      
    #     last_donation_date = donor.last_donation_date
    #     return last_donation_date

    # def calculate_donation_frequency(self, last_donation_date):
    #     # Calculate the donation frequency based on the last donation date
    #     if last_donation_date:
    #         # Assuming the last donation date is within the last year
    #         last_donation_date = datetime.combine(last_donation_date, datetime.min.time())
    #         one_year_ago = datetime.now() - timedelta(days=365)
    #         if last_donation_date >= one_year_ago:
    #             return "Frequent"  # If last donation date is within the last year
    #         else:
    #             return "Infrequent"  # If last donation date is more than a year ago
    #     else:
    #         return "No donation record"  # If no donation record exists

    # def export(self, obj):
    #     # Get the last donation date for the donor
    #     last_donation_date = self.get_last_donation_date(obj)

    #     # Calculate the donation frequency based on the last donation date
    #     donation_frequency = self.calculate_donation_frequency(last_donation_date)

    #     return donation_frequency

    def get_donation_count(self, donor):
        # Retrieve the donation count for the donor
        donation_count = DonationRecord.objects.filter(donor=donor).count()
        return donation_count

    def export(self, obj):
        # Get the donation count for the donor
        donation_count = self.get_donation_count(obj)
        return donation_count

class BloodTypeQuantityField(fields.Field):
    def export(self, obj):
        # Calculate the total quantity of each blood type available in the blood bank
        total_quantity = {
            'O+': obj.Opositive_units,
            'O-': obj.Onegative_units,
            'A+': obj.Apositive_units,
            'A-': obj.Anegative_units,
            'B+': obj.Bpositive_units,
            'B-': obj.Bnegative_units,
            'AB+': obj.ABpositive_units,
            'AB-': obj.ABnegative_units,
        }
        return total_quantity
    

# class DonationQuantityField(fields.Field):
#     def calculate_quantity(self, donation_record):
#         time_since_donation = (datetime.now().date() - donation_record.donation_date).days
#         if time_since_donation > 0:
#             quantity = 1 / time_since_donation  
#         else:
#             quantity = 1  
#         return quantity
#     def import_data(self, value, obj, **kwargs):
#         return self.calculate_quantity(obj)