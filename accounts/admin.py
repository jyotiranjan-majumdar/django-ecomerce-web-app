from django.contrib import admin

from .models import UserStripe, EmailConfirmed, UserAddress, UserDefaultAddress
# Register your models here.

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(UserDefaultAddress)

admin.site.register(UserAddress, UserAddressAdmin)

admin.site.register(UserStripe)

admin.site.register(EmailConfirmed)


