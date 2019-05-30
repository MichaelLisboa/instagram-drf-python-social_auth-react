# A one-click Instagram authentication system, using Django Rest Framework, Python Social Auth, and React JS
### The hardest part of this was getting Instagram API approval.

#### The rest of this will come as I make it...

#### Side note: While django-rest-framework-social-oauth2 is a great package, it has the worst documentation ever, so I'll write an article about my journey and how to set up React/DRF/python-social-auth soon. Hopefully that'll save you some time figuring stuff out.

1) Wasted a lot of time figuring out DRF-social-oath2. Then Like a dummy I realized Auth must be sent as headers like:

```
const token = `Bearer ${localStorage.access_token}`;
const url = `${ROOT_URL}/accounts/user/`

axios.get(url, {
    headers: {
        Authorization: token
    }
})
.then((response) =>
```

Note to self: write clearer documentation on the step-by-step of social auth and oath2
