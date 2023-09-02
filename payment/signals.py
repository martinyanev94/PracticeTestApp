from .models import Membership


def create_initial_membership():
    if not Membership.objects.filter(slug='free-plan').exists():
        Membership.objects.create(
            slug='free-plan',
            membership_type='Free',
            membership_name='Free',
            price=0,
            stripe_plan_id='free-plan',
            allowed_question=3,
            allowed_words=5000,
            allowed_tests=7
        )

    if not Membership.objects.filter(slug='pro-quarterly').exists():
        Membership.objects.create(
            slug='pro-quarterly',
            membership_type='ProfessionalQuarterly',
            membership_name='Professional',
            price=24.99,
            monthly_price=8.33,
            stripe_plan_id="price_1NiP3mEIvcSmcyn9pYJlX7FK",
            allowed_question=60,
            allowed_words=200000,
            allowed_tests=300
        )

    if not Membership.objects.filter(slug='pro-monthly').exists():
        Membership.objects.create(
            slug='pro-monthly',
            membership_type='ProfessionalMonthly',
            membership_name='Professional',
            price=12.99,
            stripe_plan_id="price_1NiP3mEIvcSmcyn90MoA1CDH",
            allowed_question=60,
            allowed_words=200000,
            allowed_tests=300
        )

    if not Membership.objects.filter(slug='pro-yearly').exists():
        Membership.objects.create(
            slug='pro-yearly',
            membership_type='ProfessionalAnnual',
            membership_name='Professional',
            price=89.99,
            monthly_price=7.49,
            stripe_plan_id="price_1NiP4ZEIvcSmcyn9B6cG8TCx",
            allowed_question=60,
            allowed_words=200000,
            allowed_tests=300
        )

    if not Membership.objects.filter(slug='premium-quarterly').exists():
        Membership.objects.create(
            slug='premium-quarterly',
            membership_type='PremiumQuarterly',
            membership_name='Premium',
            price=39.99,
            monthly_price=13.33,
            stripe_plan_id="price_1NiP5SEIvcSmcyn9xnavMCLF",
            allowed_question=120,
            allowed_words=200000,
            allowed_tests=300
        )

    if not Membership.objects.filter(slug='premium-monthly').exists():
        Membership.objects.create(
            slug='premium-monthly',
            membership_type='PremiumMonthly',
            membership_name='Premium',
            price=19.99,
            stripe_plan_id="price_1NiP5SEIvcSmcyn9hpHMOwnC",
            allowed_question=120,
            allowed_words=200000,
            allowed_tests=300
        )

    if not Membership.objects.filter(slug='premium-yearly').exists():
        Membership.objects.create(
            slug='premium-yearly',
            membership_type='PremiumAnnual',
            membership_name='Premium',
            price=139.99,
            monthly_price=11.67,
            stripe_plan_id="price_1NiP5SEIvcSmcyn9mwEJYLTG",
            allowed_question=120,
            allowed_words=200000,
            allowed_tests=300
        )
    return
