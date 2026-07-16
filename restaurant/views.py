from django.shortcuts import render
from django.http import JsonResponse
from .models import Booking, Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# Create your views here.
def index(request):
    return render(request, 'restaurant/index.html')

def create_booking(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    people = request.POST.get('people', '').strip()
    date = request.POST.get('date', '').strip()
    time = request.POST.get('time', '').strip()
    if not all([name, email, phone, people, date, time]):
        return JsonResponse({'message': 'Please fill in all fields.'}, status=400)
    try:
        Booking.objects.create(
            name=name,
            email=email,
            phone=phone,
            people=int(people),
            date=date,
            time=time
        )
    except ValueError:
        return JsonResponse({'message': 'Check the entered data.'}, status=400)
    return JsonResponse({'message': 'Your table has been booked.'})

def create_contact(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    message = request.POST.get('message', '').strip()
    if not all([name, email, phone, message]):
        return JsonResponse({'message': 'Please fill in all fields.'}, status=400)
    Contact.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message
    )
    return JsonResponse({'message': 'Your message has been sent.'})

def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')
    if not email or not password:
        return JsonResponse({'message': 'Please fill in all fields.'}, status=400)
    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({'message': 'Incorrect email or password.'}, status=400)
    login(request, user)
    return JsonResponse({'message': 'You are logged in.'})

def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')
    password_confirm = request.POST.get('password_confirm', '')
    phone = request.POST.get('phone', '').strip()
    if not all([full_name, email, password, password_confirm, phone]):
        return JsonResponse({'message': 'Please fill in all fields.'}, status=400)
    if password != password_confirm:
        return JsonResponse({'message': 'Passwords do not match.'}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'message': 'Enter a valid email address.'}, status=400)
    User = get_user_model()
    if User.objects.filter(username__iexact=email).exists():
        return JsonResponse({'message': 'A user with this email already exists.'}, status=400)
    user = User(username=email, email=email, first_name=full_name)
    try:
        validate_password(password, user)
    except ValidationError as error:
        return JsonResponse({'message': ' '.join(error.messages)}, status=400)
    user.set_password(password)
    user.save()
    login(request, user)
    return JsonResponse({'message': 'Registration completed.'})

def logout_user(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)
    logout(request)
    return JsonResponse({'message': 'You are logged out.'})