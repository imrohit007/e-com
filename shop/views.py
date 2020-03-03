from django.shortcuts import render, get_object_or_404
from shop.models import *
from django.contrib.auth.decorators	import	login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from shop.forms import *
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('shop:product_list'))

                else:
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Invalid Login')

    else:
        form = LoginForm()
        return render(request, 'shop/product/login.html', {'form': form})




def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    return render(request, 'shop/product/detail.html', {'product': product, })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            new_user = user_form.save(commit=False)
            new_user.is_active = False
            new_user.set_password(
                user_form.cleaned_data['password'])

            new_user.save()
            current_site = get_current_site(request)
            message = render_to_string('shop/registration/activate_account.html', {
                'user':new_user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            mail_subject = 'Activate your CakeShop account.'
            to_email = user_form.cleaned_data.get('email')
            email_from = settings.EMAIL_HOST_USER
            send_mail(mail_subject,
                      message, 
                      email_from, 
                      [to_email],
                      fail_silently=False,)
            
            # Create the user profile
            Profile.objects.create(user=new_user)
        return HttpResponse('Please confirm your email address to complete the registration')

    else:
        user_form = UserRegistrationForm()
        return render(request, 'shop/registration/register.html',{'user_form': user_form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None
    if new_user is not None and account_activation_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

