from django.contrib import admin
from blood_donation_app.models import *
from .resources import *
from import_export.admin import ImportExportModelAdmin,ExportActionMixin

class DonorAdmin(ImportExportModelAdmin,ExportActionMixin):
    resource_classes = [DonorResource]

class BloodBankAdmin(ImportExportModelAdmin,ExportActionMixin):
    resource_classes=[BloodBankResource]

class DonationRecordAdmin(ImportExportModelAdmin,ExportActionMixin):
    resource_classes=[DonationRecordResource]

admin.site.register(BloodType)
admin.site.register(BloodBank,BloodBankAdmin)
admin.site.register(Donor,DonorAdmin)
admin.site.register(DonationRecord,DonationRecordAdmin)
