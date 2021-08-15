from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour, Order
from django.contrib.auth import get_user
from .forms import AddOrder, UserRegistrationForm
from django.contrib import messages


def near_tours():
    near_tours = Tour.objects.all().order_by('start_date')[:3]
    return near_tours

def home(request):
    return render(request, 'home.html',{'near_tours':near_tours()})

def tour_list(request, tour_type):
    tours = []
    unique_tours = set(Tour.objects.filter(tour_type=tour_type).values_list('title', flat=True))
    for title in unique_tours:
        tours += [Tour.objects.filter(title=title)[0]]
    return render(request, 'tour_list.html', {'tours': tours,'near_tours':near_tours()})


def tour_detail(request, tour_id, tour_type):
    tour = get_object_or_404(Tour, id=tour_id)
    tours = Tour.objects.filter(title=tour.title).order_by('start_date')
    if request.method == "POST":

        form = AddOrder(request.POST)

        if form.is_valid():
            order = Order()
            order.person_numbers = form.cleaned_data['person_numbers']
            order.contact_phone = form.cleaned_data['contact_phone']
            order.user = get_user(request)
            tour = get_object_or_404(Tour, start_date=request.POST['start_date'])
            order.tour = tour


            if int(order.person_numbers) <= tour.vacant_spot:
                tour.vacant_spot = tour.vacant_spot - int(order.person_numbers)
                tour.save()
                order.save()
                return render(request, 'tour_confirm.html', {'tour': order.tour})
            else:
                messages.add_message(request, messages.INFO, 'Недостаточно свободных мест')
                redirect('tour_confirm.html', {'tour_id':tour_id})
    else:
        form = AddOrder()

    return render(request, 'tour_detail.html', {'tour':tour, 'tours':tours,'near_tours':near_tours(), 'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})

def orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'order_list.html', {'orders': orders})

