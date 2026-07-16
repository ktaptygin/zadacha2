from django.shortcuts import render
from django.http import JsonResponse
from .models import (
    Booking,
    Contact,
    Delicious,
    DeliciousCategory,
    Event,
    Speciality,
    StaticSection,
    UserProfile,
)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.conf import settings
# Create your views here.

def index(request):
    specialities = Speciality.objects.all().order_by('id')
    about_section = StaticSection.objects.filter(
        title__iexact='ABOUT US'
    ).first()
    team_section = StaticSection.objects.filter(
        title__iexact='MASTER CHEF'
    ).first()
    menu_categories = DeliciousCategory.objects.all().order_by('id')
    menu_items = Delicious.objects.filter(
        on_main=True
    ).select_related(
        'category'
    ).order_by('id')[:21]
    events = Event.objects.all().order_by('id')[:2]
    context = {
        'specialities': specialities,
        'about_section': about_section,
        'team_section': team_section,
        'menu_categories': menu_categories,
        'menu_items': menu_items,
        'events': events,
    }
    return render(request, 'restaurant/index.html', context)

def create_booking(request):
    if request.method != 'POST':
        return JsonResponse(
            {'message': 'Only POST requests are allowed.'},
            status=405
        )
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    phone = request.POST.get('phone', '').strip()
    people = request.POST.get('people', '').strip()
    date = request.POST.get('date', '').strip()
    time = request.POST.get('time', '').strip()
    if not all([name, email, phone, people, date, time]):
        return JsonResponse(
            {'message': 'Please fill in all fields.'},
            status=400
        )
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {'message': 'Enter a valid email address.'},
            status=400
        )
    try:
        people_number = int(people)
        booking_date = datetime.strptime(date, '%Y-%m-%d').date()
        booking_time = datetime.strptime(time, '%H:%M').time()
    except (TypeError, ValueError):
        return JsonResponse(
            {'message': 'Check the entered date, time and number of people.'},
            status=400
        )
    if people_number < 1 or people_number > 6:
        return JsonResponse(
            {'message': 'Choose from 1 to 6 people.'},
            status=400
        )
    if booking_date < timezone.localdate():
        return JsonResponse(
            {'message': 'Choose today or a future date.'},
            status=400
        )
    booking = Booking.objects.create(
        name=name,
        email=email,
        phone=phone,
        people=people_number,
        date=booking_date,
        time=booking_time
    )
    email_message = (
        'A new table booking has been created.\n\n'
        f'Name: {booking.name}\n'
        f'Email: {booking.email}\n'
        f'Phone: {booking.phone}\n'
        f'People: {booking.people}\n'
        f'Date: {booking.date}\n'
        f'Time: {booking.time}\n'
    )
    try:
        send_mail(
            'New table booking',
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.RESTAURANT_EMAIL],
            fail_silently=False
        )
    except Exception as error:
        print('Email sending error:', repr(error))
        return JsonResponse({
            'message': (
                'Your table has been booked, but the email could not be sent.'
            ),
            'email_sent': False,
        })
    return JsonResponse({
        'message': 'Your table has been booked.',
        'email_sent': True,
    })

def create_contact(request):
    if request.method != 'POST':
        return JsonResponse(
            {'message': 'Only POST requests are allowed.'},
            status=405
        )
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    phone = request.POST.get('phone', '').strip()
    message = request.POST.get('message', '').strip()
    if not all([name, email, phone, message]):
        return JsonResponse(
            {'message': 'Please fill in all fields.'},
            status=400
        )
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {'message': 'Enter a valid email address.'},
            status=400
        )
    Contact.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message
    )
    return JsonResponse({'message': 'Your message has been sent.'})

def login_user(request):
    if request.method != 'POST':
        return JsonResponse(
            {'message': 'Only POST requests are allowed.'},
            status=405
        )
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')
    if not email or not password:
        return JsonResponse(
            {'message': 'Please fill in all fields.'},
            status=400
        )
    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse(
            {'message': 'Incorrect email or password.'},
            status=400
        )
    login(request, user)
    return JsonResponse({'message': 'You are logged in.'})

def register_user(request):
    if request.method != 'POST':
        return JsonResponse(
            {'message': 'Only POST requests are allowed.'},
            status=405
        )
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')
    password_confirm = request.POST.get('password_confirm', '')
    phone = request.POST.get('phone', '').strip()
    if not all([full_name, email, password, password_confirm, phone]):
        return JsonResponse(
            {'message': 'Please fill in all fields.'},
            status=400
        )
    if password != password_confirm:
        return JsonResponse(
            {'message': 'Passwords do not match.'},
            status=400
        )
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {'message': 'Enter a valid email address.'},
            status=400
        )
    if len(phone) < 5:
        return JsonResponse(
            {'message': 'Enter a valid phone number.'},
            status=400
        )
    User = get_user_model()
    if User.objects.filter(username__iexact=email).exists():
        return JsonResponse(
            {'message': 'A user with this email already exists.'},
            status=400
        )
    user = User(username=email, email=email, first_name=full_name)
    try:
        validate_password(password, user)
    except ValidationError as error:
        return JsonResponse(
            {'message': ' '.join(error.messages)},
            status=400
        )
    try:
        with transaction.atomic():
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user, phone=phone)
    except IntegrityError:
        return JsonResponse(
            {'message': 'A user with this email already exists.'},
            status=400
        )
    login(request, user)
    return JsonResponse({'message': 'Registration completed.'})

def logout_user(request):
    if request.method != 'POST':
        return JsonResponse(
            {'message': 'Only POST requests are allowed.'},
            status=405
        )
    logout(request)
    return JsonResponse({'message': 'You are logged out.'})

def password_reset_request(request):
    if request.method != 'POST':
        return JsonResponse(
            {'message': 'Only POST requests are allowed.'},
            status=405
        )
    email = request.POST.get('email', '').strip().lower()
    if not email:
        return JsonResponse(
            {'message': 'Enter your email address.'},
            status=400
        )
    form = PasswordResetForm({'email': email})
    if not form.is_valid():
        return JsonResponse(
            {'message': 'Enter a valid email address.'},
            status=400
        )
    try:
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject_template_name='restaurant/password_reset_subject.txt',
            email_template_name='restaurant/password_reset_email.txt'
        )
    except Exception as error:
        print('Password reset email error:', repr(error))
        return JsonResponse(
            {'message': 'Could not send the reset email.'},
            status=500
        )
    return JsonResponse({
        'message': (
            'If an account with this email exists, '
            'a reset link has been sent.'
        )
    })