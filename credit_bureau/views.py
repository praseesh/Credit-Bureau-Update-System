from django.shortcuts import render, redirect
from .models import Question, User, UserResponse
from django.contrib.auth.decorators import login_required
from .utils import calculate_credit_score
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login

def home(request):
    return render(request, 'base.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')
        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number is already registered.")
            return redirect('register')
        user = User.objects.create_user(email=email, mobile=mobile, password=password)
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)  
                request.session['user_id'] = user.id
                request.session['user'] = user.id  
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush() 
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def questions_page(request):
    user_id = request.session.get('user_id') 
    if not user_id:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login') 
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                question = Question.objects.get(id=question_id)
                UserResponse.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected_option': value}
                )
        return redirect('results_page')
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})

def results_view(request):
    user_obj = request.user
    user_obj_id = user_obj.id
    try:
        credit_score = calculate_credit_score(user_obj.id)
    except Exception as e:
        messages.error(request, "Error calculating credit score.")
        return redirect('questions_page')  
    return render(request, 'results.html', {'credit_score': credit_score})
