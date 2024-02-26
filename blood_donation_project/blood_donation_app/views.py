from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import*
from .serializers import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .forms import *
from .forms import DonorForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .orm_filters import filter_donations_by_criteria
from datetime import datetime
# Create your views here.

def index(request):
    return render(request,'home.html')
from django.db.models import F

def update_quantity(bloodbank, bloodtype):
    try:
        blood_bank = BloodBank.objects.get(bloodbank_name=bloodbank)
    except BloodBank.DoesNotExist:
        print("Blood bank not found:", bloodbank)
        return
    if bloodtype == "O+":
        BloodBank.objects.filter(pk=blood_bank.pk).update(Opositive_units=F('Opositive_units') + 1)
    elif bloodtype == "O-":
        BloodBank.objects.filter(pk=blood_bank.pk).update(Onegative_units=F('Onegative_units') + 1)
    elif bloodtype == "A+":
        BloodBank.objects.filter(pk=blood_bank.pk).update(Apositive_units=F('Apositive_units') + 1)
    elif bloodtype == "A-":
        BloodBank.objects.filter(pk=blood_bank.pk).update(Anegative_units=F('Anegative_units') + 1)
    elif bloodtype == "B+":
        BloodBank.objects.filter(pk=blood_bank.pk).update(Bpositive_units=F('Bpositive_units') + 1)
    elif bloodtype == "B-":
        BloodBank.objects.filter(pk=blood_bank.pk).update(Bnegative_units=F('Bnegative_units') + 1)
    elif bloodtype == "AB+":
        BloodBank.objects.filter(pk=blood_bank.pk).update(ABpositive_units=F('ABpositive_units') + 1)
    elif bloodtype == "AB-":
        BloodBank.objects.filter(pk=blood_bank.pk).update(ABnegative_units=F('ABnegative_units') + 1)
    else:
        print("Invalid blood type:", bloodtype)
        print(type(bloodtype))
        return




def add_donor(request):
    if request.method == 'POST':
        donor_serializer=DonorSerializers(data=request.POST)
        if donor_serializer.is_valid():
            try:
                donor=donor_serializer.save()
                update_quantity(donor.bloodbank.bloodbank_name,donor.donor_blood_type.blood_type)
                donation_record_data = {
                    'donor': donor.donor_email,
                    'bloodbank': donor.bloodbank.bloodbank_name,
                    'donation_date': donor.last_donation_date, 
                }
                donation_record_serializer = DonationRecordSerializers(data=donation_record_data)
                print(donation_record_data)
                if donation_record_serializer.is_valid():
                    donation_record_serializer.save()
                else:
                    print(donation_record_serializer.errors)
                    print("Donation Record validation failed")
                return redirect('/')
            except IntegrityError:
                print('record exists')
                return redirect("/")
        else:
           
            existing_donor = Donor.objects.get(donor_email=request.POST['donor_email'])
            bloodbank_name = request.POST['bloodbank']
            last_donation_date = request.POST['last_donation_date']
            bloodbank_instance = BloodBank.objects.get(bloodbank_name=bloodbank_name)
            existing_donor.bloodbank = bloodbank_instance
            existing_donor.last_donation_date = last_donation_date  
            existing_donor.save()
            
            donation_record_data = {
                'donor': existing_donor.donor_email,
                'bloodbank': existing_donor.bloodbank.bloodbank_name,
                'donation_date': existing_donor.last_donation_date,
            }
            print(donation_record_data)
            donation_record_serializer = DonationRecordSerializers(data=donation_record_data)
            
            if donation_record_serializer.is_valid():
                donation_record_serializer.save()
                
                update_quantity(existing_donor.bloodbank.bloodbank_name, existing_donor.donor_blood_type.blood_type)
                return redirect('/')
            else:
                print(donation_record_serializer.errors)
                print("Donation Record validation failed")
                return redirect('/')
    
    blood_banks = BloodBank.objects.all()
    bloodtypes = BloodType.objects.all()
    return render(request, 'add_donor.html', {"bloodtypes": bloodtypes, "blood_banks": blood_banks})


@login_required(login_url='/admin_login/')
@api_view(['GET'])
def donorlist(request):
    donors=Donor.objects.all()
    serializer=DonorSerializers(donors,many=True)
    serialized_data=serializer.data
    print(serialized_data)
    return render(request,'donorlist.html',{'d':serialized_data})


def delete_donor(request,donor_email):
    donor_to_delete=get_object_or_404(Donor,donor_email=donor_email)
    donor_to_delete.delete()
    return redirect('/donorlist')



def edit_donor(request, donor_email):
    donor = get_object_or_404(Donor, donor_email=donor_email)

    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('/donorlist')
    else:
        form = DonorForm(instance=donor)
    return render(request, 'edit_donor.html', {'form': form, 'donor': donor})



@login_required(login_url='/admin_login/')
def donation_record(request):
    donation_records=DonationRecord.objects.all()
    return render(request,'donationrecord.html',{'donation_records': donation_records})


def add_bloodbank(request):
    if request.method == 'POST':
        bloodbank_serializer=BloodBankSerializers(data=request.POST)
        if bloodbank_serializer.is_valid():
            try:
                bloodbank=bloodbank_serializer.save()
                return redirect('/')
            except IntegrityError:
                print('record exists')
                return redirect("/")
        else:
            print(bloodbank_serializer.errors)
            print("validation failed")
            return redirect('/') 
    return render(request, 'add_bloodbank.html')


@login_required(login_url='/admin_login/')
def bloodbanklist(request):
    data=BloodBank.objects.all()
    return render(request,'bloodbanklist.html',{'data':data})




def admin_login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        admin=authenticate(request,username=username,password=password)
        login(request,admin)
        if admin:
            return redirect('/')
    return render(request,'admin_login.html')




class RegisterUser(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'Somethinng went wrong'})
        serializer.save()
        user=User.objects.get(username=serializer.data['username'])
        token_obj,_=Token.objects.get_or_create(user=user)
        return Response({'status':200,'payload':serializer.data,'message':'Your data is saved '})
    





def my_view(request):

    start_date = datetime(2024, 2, 5)
    end_date = datetime(2024, 2, 16)
    blood_type = 'O+'
    filtered_donations = filter_donations_by_criteria(blood_type, start_date, end_date)
    print(filtered_donations)
    return render(request, 'filtered_donations.html', {'filtered_donations': filtered_donations})


from django.shortcuts import render
from .statistics import total_blooddonation_of_each_type

def display_blood_donation_statistics(request):
    blood_type_totals_dict = total_blooddonation_of_each_type()
    return render(request, 'statistics.html', {'blood_type_totals_dict': blood_type_totals_dict})


