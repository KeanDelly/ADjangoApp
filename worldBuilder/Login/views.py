from django.shortcuts import render
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def homepage(request):
	return render(request, 'homepage.html')


def login_error(request):
	return render(request, 'loginError.html')


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('/main/')
			else:
				messages.error(request, "Invalid username or password.")
				return redirect('/loginError')
		else:
			messages.error(request, "Invalid username or password.")
			return redirect('/loginError')
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('/main')
		messages.error(request, "Unsuccessful registration. Invalid information.")
		return redirect('/loginError')
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})