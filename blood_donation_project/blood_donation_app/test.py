from django.test import TestCase,Client
from .models import BloodType,BloodBank,Donor,DonationRecord
from django.urls import reverse
from datetime import date
from .views import update_quantity
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestModels_BloodType(TestCase):
    def test_model(self):
        blood_type_instance=BloodType.objects.create(blood_type='O+')
        self.assertEqual(str(blood_type_instance),'O+')
        self.assertTrue(isinstance(blood_type_instance,BloodType))


class BloodBankModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BloodBank.objects.create(
            bloodbank_name='Test Blood Bank',
            bloodbank_location='Test Location',
            bloodbank_phone='1234567890',
            Opositive_units=100,
            Onegative_units=50,
            Apositive_units=75,
            Anegative_units=25,
            Bpositive_units=80,
            Bnegative_units=40,
            ABpositive_units=60,
            ABnegative_units=30
        )

    def test_bloodbank_name_max_length(self):
        blood_bank = BloodBank.objects.get(bloodbank_name='Test Blood Bank')
        max_length = blood_bank._meta.get_field('bloodbank_name').max_length
        self.assertEqual(max_length, 50)

    def test_bloodbank_location_max_length(self):
        blood_bank = BloodBank.objects.get(bloodbank_name='Test Blood Bank')
        max_length = blood_bank._meta.get_field('bloodbank_location').max_length
        self.assertEqual(max_length, 100)


class DonorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        blood_type = BloodType.objects.create(blood_type='A+')
        blood_bank = BloodBank.objects.create(
            bloodbank_name='Test Blood Bank',
            bloodbank_location='Test Location',
            bloodbank_phone='1234567890'
        )
        Donor.objects.create(
            donor_name='Test Donor',
            donor_email='test@example.com',
            donor_blood_type=blood_type,
            donor_phone='9876543210',
            bloodbank=blood_bank,
            last_donation_date=date.today()
        )

    def test_donor_name_max_length(self):
        donor = Donor.objects.get(donor_email='test@example.com')
        max_length = donor._meta.get_field('donor_name').max_length
        self.assertEqual(max_length, 30)

    def test_donor_email_primary_key(self):
        donor = Donor.objects.get(donor_email='test@example.com')
        self.assertTrue(donor.donor_email, 'test@example.com')

    def test_donor_phone_max_length(self):
        donor = Donor.objects.get(donor_email='test@example.com')
        max_length = donor._meta.get_field('donor_phone').max_length
        self.assertEqual(max_length, 10)


class TestView(TestCase):
    def setUp(self):
        self.client=Client()
        self.index_url=reverse('index')

    def test_index_GET(self):
        response=self.client.get(self.index_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')


class UpdateQuantityTestCase(TestCase):
    def setUp(self):
        # Create a blood bank for testing
        self.blood_bank = BloodBank.objects.create(
            bloodbank_name='Test Blood Bank',
            Opositive_units=0,
            Onegative_units=0,
            Apositive_units=0,
            Anegative_units=0,
            Bpositive_units=0,
            Bnegative_units=0,
            ABpositive_units=0,
            ABnegative_units=0
        )
    def test_update_quantity_valid_bloodtype(self):
        update_quantity(self.blood_bank.bloodbank_name, "AB+")
        updated_blood_bank = BloodBank.objects.get(bloodbank_name=self.blood_bank.bloodbank_name)
        self.assertEqual(updated_blood_bank.ABpositive_units, 1)




class EditDonorViewTest(TestCase):
    def setUp(self):
        blood_bank = BloodBank.objects.create(
            bloodbank_name='Example Blood Bank',
            bloodbank_location='Example Location',
            bloodbank_phone='1234567890',
            Opositive_units=10,
            Onegative_units=5,
            Apositive_units=8,
            Anegative_units=3,
            Bpositive_units=6,
            Bnegative_units=2,
            ABpositive_units=4,
            ABnegative_units=1
        )
        blood_type = BloodType.objects.create(blood_type='A+')

        self.donor = Donor.objects.create(
            donor_name='John Doe', 
            donor_email='john@example.com', 
            donor_phone='1234567890',
            bloodbank=blood_bank,
            donor_blood_type=blood_type,
            last_donation_date=date.today()
                
        )
    def test_edit_donor_view_get(self):
        url = reverse('edit_donor', kwargs={'donor_email': self.donor.donor_email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_edit_donor_view_post(self):
        url = reverse('edit_donor', kwargs={'donor_email': self.donor.donor_email})
        updated_data = {
            'donor_name': 'Jane Doe',
            'donor_phone': '0987654321',
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302) 
        self.donor.refresh_from_db()
        self.assertEqual(self.donor.donor_name, 'Jane Doe')
        self.assertEqual(self.donor.donor_phone, '0987654321')

    def tearDown(self):
        self.donor.delete()

class AddBloodBankViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_add_bloodbank_post(self):
        data = {
            'bloodbank_name': 'Test Blood Bank',
            'bloodbank_location': 'Test Location',
            'bloodbank_phone': '1234567890',
            'Opositive_units': 10,
            'Onegative_units': 5,
            'Apositive_units': 8,
            'Anegative_units': 3,
            'Bpositive_units': 6,
            'Bnegative_units': 2,
            'ABpositive_units': 4,
            'ABnegative_units': 1
        }
        response = self.client.post(reverse('add_bloodbank'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BloodBank.objects.filter(bloodbank_name='Test Blood Bank').exists())


class AddDonorViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.blood_bank = BloodBank.objects.create(
            bloodbank_name='Test Blood Bank',
            bloodbank_location='Test Location',
            bloodbank_phone='1234567890',
            Opositive_units=10,
            Onegative_units=5,
            Apositive_units=8,
            Anegative_units=3,
            Bpositive_units=6,
            Bnegative_units=2,
            ABpositive_units=4,
            ABnegative_units=1
        )
        self.blood_type = BloodType.objects.create(blood_type='A+')
        self.existing_donor = Donor.objects.create(
            donor_name='Test Donor',
            donor_email='test@example.com',
            donor_phone='1234567890',
            bloodbank=self.blood_bank,
            donor_blood_type=self.blood_type,
            last_donation_date=datetime.now().strftime("%Y-%m-%d")
        )

    def test_add_donor_post(self):
        data = {
            'donor_name': 'New Test Donor',
            'donor_email': 'test@example.com',
            'donor_phone': '1234567890',
            'bloodbank': self.blood_bank.bloodbank_name,
            'donor_blood_type': self.blood_type.blood_type,
            'last_donation_date': datetime.now().strftime("%Y-%m-%d")
        }
        response = self.client.post(reverse('add_donor'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Donor.objects.filter(donor_email='test@example.com').exists())

    def test_add_donor_get(self):
        response = self.client.get(reverse('add_donor'))
        self.assertEqual(response.status_code, 200)


class UrlTest(TestCase):
    def test_index_url(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_add_donor_url(self):
        response = self.client.get(reverse('add_donor'))
        self.assertEqual(response.status_code, 200)

    def test_add_bloodbank_url(self):
        response = self.client.get(reverse('add_bloodbank'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login_view_url(self):
        response = self.client.get(reverse('admin_login_view'))
        self.assertEqual(response.status_code, 200)

    def test_my_view_url(self):
        response = self.client.get(reverse('my_view'))
        self.assertEqual(response.status_code, 200)

    def test_statistics_url(self):
        response = self.client.get(reverse('display_blood_donation_statistics'))
        self.assertEqual(response.status_code, 200)
        
class DonorListViewURLTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_donorlist_view_with_authentication(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('donorlist'))
        self.assertEqual(response.status_code, 200)

    def test_donorlist_view_without_authentication(self):
        response = self.client.get(reverse('donorlist'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin_login/?next=/donorlist/', fetch_redirect_response=False)


