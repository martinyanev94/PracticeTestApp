from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from datetime import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

MEMBERSHIP_CHOICES = (
    ('EnterpriseAnnual', 'enta'),
    ('PremiumAnnual', 'prema'),
    ('ProfessionalAnnual', 'proa'),
    ('EnterpriseMonthly', 'entm'),
    ('PremiumMonthly', 'premm'),
    ('ProfessionalMonthly', 'prom'),
    ('Free', 'free')
)

MEMBERSHIP_NAMES = (
    ('Enterprise', 'ent'),
    ('Premium', 'prem'),
    ('Professional', 'pro'),
    ('Free', 'free')
)


# TODO Take price from stripe api
class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    membership_name = models.CharField(
        choices=MEMBERSHIP_NAMES,
        default='Free',
        max_length=30)
    price = models.FloatField(default=10)
    monthly_price = models.FloatField(default=10, null=True)
    stripe_plan_id = models.CharField(max_length=40)
    allowed_question = models.IntegerField()
    allowed_words = models.IntegerField(null=True)
    allowed_tests = models.IntegerField(null=True)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    user_membership, created = UserMembership.objects.get_or_create(
        user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        free_membership = Membership.objects.get(membership_type='Free')
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.membership = free_membership
        user_membership.save()


post_save.connect(post_save_usermembership_create,
                  sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)
