from .models import Membership


def create_initial_membership():
    if not Membership.objects.filter(slug='free-plan').exists():
        Membership.objects.create(
            slug='free-plan',
            membership_type='Free',
            membership_name='Free',
            price=0,
            monthly_price=0,
            stripe_plan_id='free-plan',
            allowed_question=10,
            allowed_words=200000,
            allowed_tests=7
        )

    if not Membership.objects.filter(slug='pro-quarterly').exists():
        Membership.objects.create(
            slug='pro-quarterly',
            membership_type='ProfessionalQuarterly',
            membership_name='Professional',
            price=24.99,
            monthly_price=8.33,
            stripe_plan_id="price_1NiOu8EIvcSmcyn9HzAWo6c1",
            allowed_question=30,
            allowed_words=200000,
            allowed_tests=150
        )

    if not Membership.objects.filter(slug='pro-monthly').exists():
        Membership.objects.create(
            slug='pro-monthly',
            membership_type='ProfessionalMonthly',
            membership_name='Professional',
            price=12.99,
            stripe_plan_id="price_1NiOu8EIvcSmcyn9rOUPSipU",
            allowed_question=30,
            allowed_words=200000,
            allowed_tests=150
        )

    if not Membership.objects.filter(slug='pro-yearly').exists():
        Membership.objects.create(
            slug='pro-yearly',
            membership_type='ProfessionalAnnual',
            membership_name='Professional',
            price=89.99,
            monthly_price=7.49,
            stripe_plan_id="price_1NiOu8EIvcSmcyn9QEJcmFEh",
            allowed_question=30,
            allowed_words=200000,
            allowed_tests=150
        )

    if not Membership.objects.filter(slug='premium-quarterly').exists():
        Membership.objects.create(
            slug='premium-quarterly',
            membership_type='PremiumQuarterly',
            membership_name='Premium',
            price=39.99,
            monthly_price=13.33,
            stripe_plan_id="price_1NiP2bEIvcSmcyn9Ug0OwhrF",
            allowed_question=60,
            allowed_words=200000,
            allowed_tests=300
        )

    if not Membership.objects.filter(slug='premium-monthly').exists():
        Membership.objects.create(
            slug='premium-monthly',
            membership_type='PremiumMonthly',
            membership_name='Premium',
            price=19.99,
            stripe_plan_id="price_1NiP2bEIvcSmcyn9lPj7EilS",
            allowed_question=60,
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
            stripe_plan_id="price_1NiP2bEIvcSmcyn94dq1U03a",
            allowed_question=60,
            allowed_words=200000,
            allowed_tests=300
        )
    if not Membership.objects.filter(slug='enterprise-yearly').exists():
        Membership.objects.create(
            slug='enterprise-yearly',
            membership_type='EnterpriseAnnual',
            membership_name='Enterprise',
            price=10,
            monthly_price=11.67,
            stripe_plan_id="XXX",
            allowed_question=60,
            allowed_words=200000,
            allowed_tests=300
        )
        if not Membership.objects.filter(slug='enterprise-monthly').exists():
            Membership.objects.create(
                slug='enterprise-monthly',
                membership_type='EnterpriseAnnual',
                membership_name='Enterprise',
                price=10,
                monthly_price=11.67,
                stripe_plan_id="XXX",
                allowed_question=60,
                allowed_words=200000,
                allowed_tests=300
            )
        if not Membership.objects.filter(slug='enterprise-quarterly').exists():
            Membership.objects.create(
                slug='enterprise-quarterly',
                membership_type='EnterpriseQuarterly',
                membership_name='Enterprise',
                price=10,
                monthly_price=11.67,
                stripe_plan_id="XXX",
                allowed_question=60,
                allowed_words=200000,
                allowed_tests=300
            )
    return
