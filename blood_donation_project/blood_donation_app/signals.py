from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.contrib.auth.models import User 
from .models import BloodBank
from django.dispatch import receiver
from django.db.models.signals import pre_init,pre_save,pre_delete,post_delete,post_save




@receiver(user_logged_in,sender=User)
def login_success(sender,request,user,**kwargs):
    print("______________")
    print("Logged-in Signal....Run Intro..")
    print("Sender:",sender)
    print("Request",request)
    print("User:",user)
    print(f'Kwargs:{kwargs}')

# user_logged_in.connect(login_success,sender=User)

def logout_success(sender,request,user,**kwargs):
    print("______________")
    print("Logotut Signal....Run Intro..")
    print("Sender:",sender)
    print("Request",request)
    print("User:",user)
    print(f'Kwargs:{kwargs}')

user_logged_out.connect(logout_success,sender=User)


@receiver(user_login_failed)
def login_failed(sender,credentials,request,**kwargs):
    print("______________")
    print("Login Failed..")
    print("Sender:",sender)
    print("Request",request)
    print("Credentials",credentials)
    print(f'Kwargs:{kwargs}')



@receiver(pre_save,sender=User)
def at_beginning_save(sender,instance,**kwargs): 
    print("______________")
    print("Pre save signal")
    print("Sender:",sender)
    print("Instance",instance)
    print(f'Kwargs:{kwargs}')

    

@receiver(post_save, sender=User) 
def at_end_user(sender,instance,created,**kwargs):
    if created:
        print("----------------------")
        print("Post Save Signal.....")
        print("New Record")
        print("Sender:",sender)
        print("Instance:",instance)
        print("Created:",created)
        print(f'Kwargs:{kwargs}')
    else:
        print("-------------------")
        print("Post save signal")
        print("Update")
        print("Sender:",sender)
        print("Instance:",instance)
        print("Created",created)
        print(f"kwargs:{kwargs}")


@receiver(post_save, sender=BloodBank)
def check_blood_units(sender, instance, **kwargs):
    if any([
        instance.Opositive_units is not None and instance.Opositive_units > 10,
        instance.Onegative_units is not None and instance.Onegative_units > 10,
        instance.Apositive_units is not None and instance.Apositive_units > 10,
        instance.Anegative_units is not None and instance.Anegative_units > 10,
        instance.Bpositive_units is not None and instance.Bpositive_units > 10,
        instance.Bnegative_units is not None and instance.Bnegative_units > 10,
        instance.ABpositive_units is not None and instance.ABpositive_units > 10,
        instance.ABnegative_units is not None and instance.ABnegative_units > 10
    ]):
        print("----------------------------------------------------------------------------")
        print("Blood units in one of the categories exceeded 10 in", instance.bloodbank_name)


