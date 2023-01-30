from django.contrib import admin

# Register your models here.
from base.models import User, foodlist, foodlike

admin.site.register([User,foodlist,foodlike])

