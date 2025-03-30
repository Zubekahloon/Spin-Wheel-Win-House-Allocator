
from django.shortcuts import render, redirect, HttpResponse
from .models import User, AssignedHouse
from django.contrib import messages
import os, csv
from django.http import JsonResponse
from django.conf import settings



def index(request):
    return render(request, "index.html")

def add_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        age = request.POST.get("age")

        if name and email and age:
            user, created = User.objects.get_or_create(email=email, defaults={"name": name, "age": age})
            if created:
                messages.success(request, "User added successfully!")
            else:
                messages.warning(request, "User with this email already exists!")
        else:
            messages.error(request, "All fields are required!")

        return redirect("display_users")

    return render(request, "add_user.html")

def display_users(request):
    users = User.objects.all()
    return render(request, "display_users.html", {"users": users})


ASSIGNED_HOUSES_FILE = os.path.join(settings.MEDIA_ROOT, "data/assigned_house_to_user.csv")
HOUSE_LIST_FILE = os.path.join(settings.MEDIA_ROOT, "data/house_no1.csv")

def assign_house_to_user(request, house_number):
    try:
        assigned_house = AssignedHouse.objects.filter(house_number=house_number).select_related('user').first()

        if not assigned_house:
            return JsonResponse({"success": False, "message": "House not assigned to any user!"}, status=400)

        user = assigned_house.user  


        if os.path.exists(ASSIGNED_HOUSES_FILE):
            with open(ASSIGNED_HOUSES_FILE, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if str(house_number) in row:
                        return JsonResponse({"success": False, "message": f"House No {house_number} is already recorded!"}, status=400)

       
        os.makedirs(os.path.dirname(ASSIGNED_HOUSES_FILE), exist_ok=True)
        with open(ASSIGNED_HOUSES_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([user.name, user.email, house_number])

       
        if os.path.exists(HOUSE_LIST_FILE):
            with open(HOUSE_LIST_FILE, "r", newline="") as file:
                houses = list(csv.reader(file))

           
            updated_houses = [row for row in houses if row and row[0] != str(house_number)]

         
            with open(HOUSE_LIST_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_houses)

        return JsonResponse({
            "success": True,
            "user_name": user.name,
            "email": user.email,
            "house_number": house_number
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)



def assign_house(request):
    error = ""
    
    if request.method == "POST":
        user_id = request.POST.get("user")
        house_number = request.POST.get("house_number")

        if not user_id or not house_number:
            error = "Please fill all fields!"

        else:
            user = User.objects.get(id=user_id)
            house_number = int(house_number)

            if AssignedHouse.objects.filter(house_number=house_number).exists():
                error = f"House No {house_number} is already assigned!"
            else:
                AssignedHouse.objects.create(user=user, house_number=house_number)
                return redirect("assign_house") 

    users = User.objects.all()
    return render(request, "assign_house.html", {"users": users, "error": error})

