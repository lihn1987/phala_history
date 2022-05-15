from django.contrib import admin
from start_app.models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "super_user"
    )