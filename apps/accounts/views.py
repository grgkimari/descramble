from django.shortcuts import render
from .forms import SignupForm,LoginForm

def register_view(request):
    form = SignupForm(request.POST)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            msg = 'You have successfully registered.'
    
    return render(request,'accounts/register.html',{'form' : form, 'msg' : msg})

def login_view(request):
	form = LoginForm(request.POST)
	msg = None
	if request.method == 'POST':
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user:
				login(request, user)
				return redirect('homePage')
			else:
				msg = "Invalid Credentials"

		else:
			msg = "Error validating form"
	else:
		msg = "Form not submitted"
	return render(request,'accounts/login.html',{'form' : form, 'msg' : msg} )