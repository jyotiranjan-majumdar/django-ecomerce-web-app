import stripe
import random
import hashlib, binascii
from django.shortcuts import render, HttpResponseRedirect 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string


stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()

class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("UserAddress", related_name="user_address_shipping_default" , on_delete=models.CASCADE, null=True, blank=True)
    billing = models.ForeignKey("UserAddress", related_name="user_address_billing_default" , on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self):
        return str(self.user.username)

class UserAddressManager(models.Manager):
    def get_billing_addresses(self, user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120,null=True,blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120,null=True,blank=True)
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now= False)
    updated = models.DateTimeField(auto_now_add=False, auto_now= True)

    def __unicode__(self):
        return str(self.user.username)
    
    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.address,self.city,self.state,self.country,self.zipcode,)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated', '-timestamp']


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=120, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        #send email
        activation_url = "%s%s" %(settings.SITE_URL, redirect("activation_view", args=[self.activation_key]))
        context = {
            "activation_key": self.activation_key,
            "activation_url": activation_url,
            "user": self.user.username,
        }
        message = render_to_string("accounts/activation_message.txt", context)
        subject = "Activate your Email"
        #print(message)
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)



def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email = str(user.email)
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()
      

def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        get_create_stripe(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            short_hash = hashlib.pbkdf2_hmac('sha1', b'password', b'salt', 100000)
            activation_key = hashlib.sha1(short_hash).hexdigest()
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            email_confirmed.activate_user_email()

            
            
post_save.connect(user_created, sender=User)



