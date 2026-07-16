from django.shortcuts import render
from django.http import JsonResponse
from .models import Booking, Contact
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