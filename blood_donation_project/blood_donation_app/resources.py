from import_export import resources,fields,widgets
from .models import *
from datetime import datetime

from .export_field import DonationFrequencyField,BloodTypeQuantityField
class DonorResource(resources.ModelResource):
    bloodbank = fields.Field(
        column_name='bloodbank',
        attribute='bloodbank',
        widget=widgets.ForeignKeyWidget(BloodBank, 'bloodbank_name')
    )

    blood_type = fields.Field(
        column_name='blood_type',
        attribute='donor_blood_type',
        widget=widgets.ForeignKeyWidget(BloodType, 'blood_type')
    )

    frequency = DonationFrequencyField(column_name='frequency', attribute='donor', readonly=True)
    class Meta:
        model = Donor
        fields = ('donor_name', 'donor_email', 'blood_type', 'bloodbank', 'last_donation_date', 'frequency')



class BloodBankResource(resources.ModelResource):
    blood_type_quantity = BloodTypeQuantityField(column_name='Blood Type Quantity')
    class Meta:
        model = BloodBank
        fields = ('bloodbank_name', 'bloodbank_location', 'bloodbank_phone', 'blood_type_quantity')


class DonationRecordResource(resources.ModelResource):
    donor=fields.Field(
        column_name='donor_name',
        attribute='donor',
        widget=widgets.ForeignKeyWidget(Donor, 'donor_name')
    )
    bloodbank=fields.Field(
        column_name="bloodbank_name",
        attribute="bloodbank",
        widget=widgets.ForeignKeyWidget(BloodBank,"bloodbank_name")
    )

    quantity = fields.Field(column_name='quantity', attribute=None)
    class Meta:
        model = DonationRecord
        fields=('donor_name','bloodbank_name','donation_date','quantity')
        
    def dehydrate_quantity(self, donation_record):
        time_since_donation = (datetime.now().date() - donation_record.donation_date).days
        print(time_since_donation,"hi")
        if time_since_donation > 0:
            quantity = 1 / time_since_donation
        else:
            quantity = 1
        return quantity

    
