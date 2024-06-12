from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request, f"User {username} created!")
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    return render(request, 'accounts/login.html')