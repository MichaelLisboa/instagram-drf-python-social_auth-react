from django.conf import settings
from django.db import models
from datetime import datetime
import stripe


class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
        ('enterprise', 'Enterprise'),
        ('professional', 'Professional'),
        ('individual', 'Individual'),
        ('all-access', 'All Access'),
        ('free', 'Influencer')
    )

    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        max_length=30,
        default='free'
    )
    display_name = models.CharField(max_length=55, blank=True)
    details = models.CharField(max_length=254, blank=True)
    description = models.CharField(max_length=254, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_plan_id = models.CharField(max_length=55)
    active = models.BooleanField(default=True)

    def details_as_list(self):
        return self.details.split(',')

    class Meta:
        managed = False

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)
    stripe_customer_id = models.CharField(max_length=55)
    membership = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        managed = False

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=55)
    active = models.BooleanField(default=True)

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

    class Meta:
        managed = False

    def __str__(self):
        return self.user_membership.user.username
