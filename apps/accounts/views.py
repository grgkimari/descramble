from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def register_view(request):
	form = SignupForm()
	msg = None
	if request.method == 'POST':
		msg = 'Post request received'
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			msg = 'You have successfully registered.'
			return redirect('homePage')
		else:
			msg = 'Error creating user'
    
	return render(request,'accounts/register.html',{'form' : form, 'msg' : msg})

def login_view(request):
	form = LoginForm()
	msg = None
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user:
				login(request, user)
				return redirect('homePage')
			else:
				msg = "Invalid Credentials."

		else:
			msg = "Error validating form."
	else:
		msg = "Form not submitted"
	return render(request,'accounts/login.html',{'form' : form, 'msg' : msg} )

def logout_view(request):
	logout(request)
	return redirect('homePage')

@login_required(login_url = 'login')
def edit_user(request):
	if request.method == 'POST':
		level = request.POST.get('level')
		request.user.level = level
		request.user.save()
		return redirect('homePage')
	else:
		return render(request,'accounts/edit_user.html')