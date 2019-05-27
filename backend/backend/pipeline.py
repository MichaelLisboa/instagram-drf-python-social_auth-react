import os
from accounts.models import CelebModel, Profile
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from memberships.models import Membership, Subscription, UserMembership
import stripe

User = get_user_model()
stripe.api_key = os.environ['STRIPE_SECRET']


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    USER_FIELDS = ['username', 'email']

    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return

    _user = kwargs['response']['data']

    fields.update({
        "username": _user['username'],
        "first_name": details['first_name'],
        "last_name": details['last_name'],
        "email": details['email']
    })

    instance = strategy.create_user(**fields)

    try:
        profile = instance.profile
        profile.fb_id = kwargs['uid']
        profile.slug = slugify(_user['username'])
        profile.profile_pic = _user['profile_picture']
        profile.bio = kwargs['bio'] if 'bio' in kwargs else '',
        profile.save()
    except Exception as e:
        import traceback
        errorLine = str(traceback.format_exc())
        print("UPDATE PROFILE ERROR", e, errorLine)
        pass

    data = {
        'is_new': True,
        'user': instance
    }

    return data


def link_profile(request, backend, strategy, details, response,
                 user, is_new, *args, **kwargs):
    print("REQUEST", request)
    if backend.name == 'instagram':
        user_data = response.get('data')
        if is_new:
            user.username = user_data['username']
            user.save()
        profile = user.profile

        influencer_data = {
            "profile": profile,
            "name": user_data['full_name'],
            "slug": slugify(user_data['username']),
            "ig_handle": user_data['username'],
            "link": f"https://www.instagram.com/{user_data['username']}",
            "followers": user_data['counts']['followed_by'],
            "profile_pic": user_data['profile_picture']
        }

        influencer, created = (
            CelebModel
            .objects
            .update_or_create(
                name=user_data['full_name'],
                ig_handle=user_data['username'],
                defaults=influencer_data,
            )
        )


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
            membership_type=membership_type
            )
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


def create_subscription(request, details, response, user, is_new):

    if not is_new:
        return

    user_data = response.get('data')

    selected_membership_type = 'free'

    selected_membership_qs = Membership.objects.filter(
        membership_type=selected_membership_type)

    # assign to the session
    request.session['selected_membership_type'] = selected_membership_qs.first()
    publish_key = os.environ['STRIPE_PUBLISHABLE']

    selected_membership = get_selected_membership(request)
    print("SELECTED MEMBERSHIP", selected_membership)

    name = user_data['full_name']

    token = (request.POST['stripeToken']
             if 'stripeToken' in request.POST
             else None)

    _cus = {
        "email": form.cleaned_data['email'],
        "description": user_data['full_name']
    }

    _sub = {"items": [{'plan': selected_membership.stripe_plan_id}]}

    cus = stripe.Customer.create(**_cus)
    cus.save()
    _sub['customer'] = cus.id

    subscription = stripe.Subscription.create(**_sub)

    user.is_active = True
    user.save()
    # user.profile.save()

    user_membership, created = (
            UserMembership.objects.get_or_create(user=user)
            )
    user_membership.membership = selected_membership
    user_membership.stripe_customer_id = cus.id
    user_membership.save()
    sub, created = (
            Subscription.objects.get_or_create(
                    user_membership=user_membership)
            )
    sub.stripe_subscription_id = subscription.id
    sub.active = True
    sub.save()

    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership,
        'membership_name': selected_membership.display_name
    }

    return render(
        request,
        'accounts/linked_profile.html',
        context=context
    )
