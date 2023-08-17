from django.shortcuts import  render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from .forms import NewUserForm, EditProfileForm, EditRoleForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate


# Create your views here.
def home(request):
    return render(request, 'floatapp/home.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/profile')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "floatapp/login.html",
                    context={"form":form})

def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successfully!")
            return redirect('/login')
    else:
        form = NewUserForm()

        args = {'form': form}
        return render(request, 'floatapp/register.html', args)

def profile(request):
    args = {'user': request.user}
    return render(request, 'floatapp/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Changed Successfully!")
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'floatapp/edit_profile.html', args)

#def edit_role(request):
#    if request.method == 'POST':
#        form = EditRoleForm(request)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully!")
            return redirect('/profile')
        else:
            messages.error(request, "Wrong Old Password. Enter Correct Old Password!")
            return redirect('/profile/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'floatapp/change_password.html', args)

def reset_password(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "floatapp/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

					messages.success(request, 'Mail regarding password reset had been sent.')
					return redirect ("/")
			messages.error(request, "Invalid Email has been entered.  Please Enter a valid one!")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="floatapp/password/password_reset.html", context={"password_reset_form":password_reset_form})
