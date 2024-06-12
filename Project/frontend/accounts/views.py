from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"User {username} created!")
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
        messages.success(request, f"User {username} not created!")

    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    return render(request, 'accounts/login.html')