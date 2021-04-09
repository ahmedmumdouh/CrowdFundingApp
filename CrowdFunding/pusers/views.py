from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from pusers.forms import RegistraionForm, LoginForm, UpdateUserForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from pusers.models import PUsers
import datetime
# from projects.models import Categories, Projects, Project_donations, Tags
# from projects.forms import NewProject
# from django.db.models import Q, Avg, Sum
from django.template.defaulttags import register

# Create your views here.


def test(request):
    return HttpResponse("Should route to web app home page")
    # return render(request, "users/home.html", context)


def register_view(request):
    context = {}
    if request.POST:
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_email(
                user,
                get_current_site(request),
                form.cleaned_data.get("email"),
                "pusers/acc_active_email.html",
                "(CrowdFunding): Activate your account.",
            )
            return render(request, "pusers/signup_link_email.html", {"active_code": -1})
        else:
            context["form"] = form
    else:
        form = RegistraionForm()
        context["form"] = form
    return render(request, "pusers/register.html", context)


def activate(request, uidb64, time):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("user id : ", uid)
        time_sent = force_text(urlsafe_base64_decode(time))
        user = PUsers.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        if user.is_active == False:
            email_sent_at = time_sent
            date_diffrince = (
                datetime.datetime.now()
                - datetime.datetime.strptime(email_sent_at,
                                             "%Y-%m-%d %H:%M:%S.%f")
            ).seconds / 60

            if date_diffrince < (24 * 60):
                user.is_active = True
                user.save()
                return render(
                    request, "pusers/signup_link_email.html", {"active_code": 1}
                )
            else:
                current_site = get_current_site(request)
                email = user.email
                send_email(
                    user,
                    current_site,
                    email,
                    "pusers/acc_active_email.html",
                    "Activate your account.",
                )
                return render(
                    request, "pusers/signup_link_email.html", {"active_code": 0}
                )
        else:
            return render(request, "pusers/signup_link_email.html", {"active_code": 2})
    else:
        return render(request, "pusers/signup_link_email.html", {"active_code": 3})


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("index")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("index")

    else:
        form = LoginForm()

    context["form"] = form

    return render(request, "pusers/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("index")


def send_email(user, current_site, email, email_body, email_subject):
    mail_subject = email_subject
    message = render_to_string(
        email_body,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "time": urlsafe_base64_encode(force_bytes(datetime.datetime.now())),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()





def user_profile_update(request):
    form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
    if request.POST:
        if form.is_valid():
            print("photo from form is :", form.cleaned_data["photo"])
            request.user.photo = form.cleaned_data["photo"]
            form.save()
            return redirect(reverse("pusers:profile"))
    else:
        form = UpdateUserForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "date_birth": request.user.date_birth,
                "facebook_link": request.user.facebook_link,
                "country": request.user.country,
            }
        )
    context = {"form": form}
    return render(request, "pusers/user_profile_update.html", context=context)


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse("pusers:login"))
    return render(request, "pusers/user_profile.html")


def send_delete_email(request):
    if request.POST:
        email = request.user.email
        password = request.POST.get('confirm_pass')  
        print(password)
        user = authenticate(email=email, password=password)
        if user:
            user = request.user
            current_site = get_current_site(request)
            email = user.email
            email_subject = "Delete your account"
            email_body = "pusers/acc_del_email.html"
            send_email(user, current_site, email, email_body, email_subject)
            return render(request, "pusers/delete_account_email.html", {"delete_code": -1})
    return  render(request, "pusers/user_profile.html")



def delete_account(request, uidb64, time):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        time_sent = force_text(urlsafe_base64_decode(time))
        user = PUsers.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        email_sent_at = time_sent
        date_diffrince = (
            datetime.datetime.now()
            - datetime.datetime.strptime(email_sent_at, "%Y-%m-%d %H:%M:%S.%f")
        ).seconds / 60

        if date_diffrince < (24 * 60):
            user.delete()
            logout(request)
            return render(
                request, "pusers/delete_account_email.html", {"delete_code": 1}
            )
        else:
            current_site = get_current_site(request)
            email = user.email
            send_email(
                user,
                current_site,
                email,
                "pusers/acc_del_email.html",
                "Delete your account.",
            )
            return render(
                request, "pusers/delete_account_email.html", {"delete_code": 0}
            )
    else:
        return render(request, "pusers/delete_account_email.html", {"delete_code": 2})
















from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "pusers/password_reset_email.txt"
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
						send_mail(subject, email, 'ahmedmumdouh94@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="pusers/password_reset.html", context={"password_reset_form":password_reset_form})