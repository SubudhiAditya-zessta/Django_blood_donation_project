from django.apps import AppConfig


class BloodDonationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blood_donation_app'

    def ready(self):
        import blood_donation_app.signals
