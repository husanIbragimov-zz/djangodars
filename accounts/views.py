from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def index_view(request):

    return redirect('/articles/')


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # print(request.POST)
        if form.is_valid():
            user = form.get_user()

            login(request, user)
            return redirect('/articles')
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username: ', username)
        print('password: ', password)
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'username or password invalid')
            return redirect('login_view')
        login(request, user)
        return redirect('/articles')
    """

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login')

    return render(request, 'accounts/logout.html', {})


def user_register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/login')
    return render(request, 'accounts/register.html', {'form': form})
