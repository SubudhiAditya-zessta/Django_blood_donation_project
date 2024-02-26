from django.db import models


from storages.backends.s3boto3 import S3Boto3Storage

class S3MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
# Create your models here.
    
class BloodType(models.Model):
    blood_type=models.CharField(max_length=20)

    def __str__(self):
        return self.blood_type




class BloodBank(models.Model):
    bloodbank_name=models.CharField(max_length=50,primary_key=True)
    bloodbank_location=models.CharField(max_length=100)
    bloodbank_phone=models.CharField(max_length=10)
    Opositive_units=models.IntegerField(null=True, blank=True)
    Onegative_units=models.IntegerField(null=True, blank=True)
    Apositive_units=models.IntegerField(null=True, blank=True)
    Anegative_units=models.IntegerField(null=True, blank=True)
    Bpositive_units=models.IntegerField(null=True, blank=True)
    Bnegative_units=models.IntegerField(null=True, blank=True)
    ABpositive_units=models.IntegerField(null=True, blank=True)
    ABnegative_units=models.IntegerField(null=True, blank=True)




class Donor(models.Model):
    donor_name=models.CharField(max_length=30)
    donor_photo=models.ImageField(upload_to='media',storage=S3MediaStorage(),null=True,blank=True)
    donor_email=models.EmailField(primary_key=True)
    donor_blood_type=models.ForeignKey(BloodType,on_delete=models.CASCADE,)
    donor_phone=models.CharField(max_length=10)
    bloodbank=models.ForeignKey(BloodBank,on_delete=models.CASCADE)
    last_donation_date=models.DateField(default=None)

    def __str__(self):
        return self.donor_name







class DonationRecord(models.Model):
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE,to_field="donor_email")
    bloodbank=models.ForeignKey(BloodBank,on_delete=models.CASCADE,to_field="bloodbank_name")
    donation_date=models.DateField()
    def __str__(self):
        return self.donor.donor_name+" "+self.bloodbank.bloodbank_name