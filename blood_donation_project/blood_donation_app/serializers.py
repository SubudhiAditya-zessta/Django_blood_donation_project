from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from django.contrib.auth.models import User 




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']

    def create(self,validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user 


class BloodTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model=BloodType
        fields="__all__"
    

class BloodBankSerializers(serializers.ModelSerializer):
    class Meta:
        model=BloodBank
        fields="__all__"

class DonorSerializers(serializers.ModelSerializer):
    donor_blood_type = serializers.SlugRelatedField(slug_field="id",queryset=BloodType.objects.all())
    bloodbank = serializers.SlugRelatedField(slug_field='bloodbank_name', queryset=BloodBank.objects.all())
    class Meta:
        model=Donor
        fields="__all__"

class DonationRecordSerializers(serializers.ModelSerializer):
    donor=serializers.SlugRelatedField(slug_field="donor_email",queryset=Donor.objects.all())
    bloodbank = serializers.SlugRelatedField(slug_field='bloodbank_name', queryset=BloodBank.objects.all())
    class Meta:
        model=DonationRecord
        fields="__all__"

