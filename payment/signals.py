# signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Membership

@receiver(post_migrate)
def create_initial_membership(sender, **kwargs):
    if Membership.objects.filter(slug='free-plan').exists():
        return
    Membership.objects.create(
        slug='free-plan',
        membership_type='Free',
        price=0,
        stripe_plan_id='free-plan',
        allowed_question=3,
        allowed_words=5000,
        allowed_tests=7
    )

#TODO Create the rest of the memberships