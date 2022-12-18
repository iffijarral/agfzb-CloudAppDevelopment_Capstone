from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.utils.formats import get_format
from django.utils.dateformat import DateFormat
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    print("Hej I am inside about")
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):    
    print("Hej I am inside contact")
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/DK-Student_mySpace/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        #dealerships = get_dealer_by_state(url, st="TX")
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}    
    if request.method == 'GET':
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/DK-Student_mySpace/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context['reviews'] = reviews
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        cars = CarModel.objects.all()
        context['dealerId'] = dealer_id
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':    
        name = request.POST['name']
        purchasecheck = bool(request.POST.get('purchasecheck', False))                    
        car_id = request.POST['car']
        purchase_date = request.POST['purchasedate']
        purchase_date = datetime.strptime(purchase_date, '%Y-%m-%dT%H:%M')
        purchase_date = purchase_date.strftime('%d/%m/%Y')
        #iso_format = datetime.utcnow().isoformat()
        reviews = request.POST['content']
        car = CarModel.objects.get(id = car_id)                
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/DK-Student_mySpace/dealership-package/post-review"
        if request.user.is_authenticated:
            review = dict()
            review['name'] = name
            review['dealership'] = dealer_id
            review['review'] = reviews
            review['purchase'] = purchasecheck
            review['purchase_date'] = purchase_date
            review['car_make'] = car.make.name
            review['car_model'] = car.name
            review['car_year'] = car.year.strftime("%Y")
            post_result = post_request(url, review, dealerId=dealer_id)
            context['post_result'] = post_result
            context['dealerId'] = dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        else: 
            return HttpResponse("You are not logged in", status=400)
        
        


