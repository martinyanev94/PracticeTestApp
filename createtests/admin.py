from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserTest  # Import your User and UserTest models

class UserTestInline(admin.TabularInline):
    model = UserTest
    extra = 0  # To display existing UserTests without additional empty forms
    fields = ('header', 'subtitle', 'institution', )  # Customize the fields to display

class CustomUserAdmin(UserAdmin):
    inlines = [UserTestInline]

# Replace the default UserAdmin with the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ('header', 'subtitle', 'institution', 'created_at', 'owner')
    list_filter = ('owner',)

