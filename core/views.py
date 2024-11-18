
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from .models import Name
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NameSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class Signup(generics.CreateAPIView):
    serializer_class = NameSerializer
        
    def post(self, request):
            email = request.data.get('email')
            username = request.data.get('username')
            password = request.data.get('password')

            if email and username and password:
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)  

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



@login_required(login_url="/login_view/")
def index_view(request):
    return render(request, 'index.html')


def abc(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if email and username and password:
            if not Name.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                
                user = Name(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Your account is successfully created!')
                return redirect('abc')
            else:
                messages.error(request, 'Username already exists. Please try a different one.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login1.html')

@login_required(login_url="/login_view/")
def logout_view(request):
    logout(request)
    return redirect('login')


def update_user(request, id):   
    queryset = Name.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        queryset.username = username
        queryset.email = email

        queryset.save()
        messages.success(request, 'User updated successfully.')
        return redirect("index_two")

    context = {'Name': queryset}
    return render(request, "update_user.html", context)  


def delete_user(request, id):
    try:
        queryset = Name.objects.get(id=id)
        queryset.delete()
        messages.success(request, 'User deleted successfully.')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
    
    return redirect("index_two")


ADMIN_USERNAME = 'adminsingh' 
ADMIN_PASSWORD = '123@singh'
def Adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect('index_two')  
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('Adminlogin') 

    return render(request, 'login2.html')

def index_two(request):
    if request.method == "POST":
        
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')


        Name.objects.create(
            username = username,
            password = password,
            email = email,
        )
        return redirect ("index1")
    queryset = Name.objects.all()


    context = {'Names': queryset}

    return render(request, 'index1.html', context)

def logout_admin(request):
    logout(request)
    return redirect('Adminlogin')


