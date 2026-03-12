# views.py

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from django. http import HttpResponse
from .forms import ContactForm
from .models import Contact
import uuid
from .models import Student
import logging
from .models import Course


logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import LoginForm
from .models import StudentProfile
from django.utils.crypto import get_random_string
from .forms import ForgotPasswordForm
from django.contrib.auth.decorators import login_required
from .forms import CourseSignupForm
from .forms import ProfileEditForm




# Create your views here.
def home(request):
    images=[
        'scope-india-aws-certification-course.jpg',
        'scope-india-azure-certification-course.jpg',
        'scope-india-digital-marketing-course.jpg',
        'scope-india-dotnet-core-full-stack-course.jpg',
        'scope-india-java-full-stack-course.jpg',
        'scope-india-mean-mern-stack-course.jpg',
        'scope-india-python-full-stack-course.jpg',
    ]
    return render(request, 'myapp/home.html',{'images':images})




def contact(request):
    sent = False
    error = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            try:
                full_message = f"From: {name} <{email}>\n\n{message}"
                send_mail(subject, full_message, email, ['itsmepchandru@gmail.com'])
                Contact.objects.create(name=name, email=email, subject=subject, message=message)
                sent = True
            except BadHeaderError:
                error = True
        else:
            error = True  # one or more fields were missing

    return render(request, 'myapp/contact.html', {'sent': sent, 'error':error})


   


            

def about(request):
    return render(request, 'myapp/about.html')

def courses(request):
    return render(request, 'myapp/courses.html')

def registration(request):
    return render(request, 'myapp/registration.html')



def registration_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            if User.objects.filter(username=email).exists():
                return HttpResponse("A user with this email already exists.")

            # Collect other data
            full_name = request.POST.get('full_name')
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            qualification = request.POST.get('qualification')
            mobile_number = request.POST.get('mobile_number')
            guardian_name = request.POST.get('guardian_name')
            guardian_occupation = request.POST.get('guardian_occupation')
            guardians_mobile = request.POST.get('guardians_mobile')
            course = request.POST.get('course')
            training_mode = request.POST.get('training_mode')
            training_location = request.POST.get('training_location')
            preferred_timings = request.POST.get('preferred_timings')
            address = request.POST.get('address')
            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')
            zip_code = request.POST.get('zip_code')

            # Create user
            temp_password = get_random_string(length=8)
            user = User.objects.create_user(username=email, email=email, password=temp_password)

            # Create student
            student = Student.objects.create(
                user=user,
                full_name=full_name,
                date_of_birth=date_of_birth,
                gender=gender,
                qualification=qualification,
                mobile_number=mobile_number,
                email=email,
                guardian_name=guardian_name,
                guardian_occupation=guardian_occupation,
                guardians_mobile=guardians_mobile,
                course=course,
                training_mode=training_mode,
                training_location=training_location,
                preferred_timings=preferred_timings,
                address=address,
                country=country,
                state=state,
                city=city,
                zip_code=zip_code,
            )

            StudentProfile.objects.create(user=user, is_temp_password=True)

            # Send mail
            verify_link = request.build_absolute_uri(f"/verify/{student.verification_token}/")
            send_mail(
                subject='Confirm Your Registration',
                message=f'Click the link to verify your email: {verify_link}\n\nYour temporary password is: {temp_password}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            return render(request, 'myapp/registration_success.html')

        except IntegrityError as e:
            return HttpResponse("A user with this email already exists.")
        except Exception as e:
            return HttpResponse(f"DEBUG:Registration failed with error - {e}")

    return render(request, 'myapp/registration.html')


def verify_email(request, token):
    try:
        student = Student.objects.get(verification_token=token)
        student.is_verified = True
        student.save()
        return render(request, 'myapp/verification_success.html')
    except Student.DoesNotExist:
        return render(request, 'myapp/verification_failed.html')
    
def course_detail(request,slug):
    course=get_object_or_404(Course, slug=slug)
    return render(request, 'myapp/course_detail.html',{'course':course})    




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            keep_logged_in = form.cleaned_data['keep_logged_in']
 
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return redirect('login')

            user = authenticate(request, username=user.username, password=password)

            if user:
                login(request, user)
                if keep_logged_in:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Session expires on browser close

                # Check if temp password
                if hasattr(user, 'studentprofile') and user.studentprofile.is_temp_password:
                    return redirect('reset_temp_password')  # redirect to password reset
                return redirect('dashboard_view')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html',{'form':form})

def send_temp_password(user):
    temp_pasword=get_random_string(length=8)
    user.set_password(temp_pasword)
    user.save()
    profile=user.studentprofile
    profile.is_temp_password=True
    profile.save()

    send_mail(
        subject="Temporary Password",
        message=f"Use this temporary password to login: {temp_pasword}",
        from_email="vishnuprakash8138@gmail.com",recipient_list=[user.email],
    )

def reset_temp_password(request):
    if request.method =='POST':
        new_password=request.POST['new_password']
        user=request.user
        user.set_password(new_password)
        user.save()
        user.studentprofile.is_temp_password=False
        user.studentprofile.save()
        messages.success(request,'Password updated successfully,Please login again.')
        logout(request)
        return redirect('login')
    return render(request,'myapp/reset_temp_password.html')


def logout_view(request):
    logout(request)
    messages.success(request,"Logged out successfully.")
    return redirect('login')


def forgot_password_view(request):
    if request.method =='POST':
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            try: 
                user=User.objects.get(email=email)
                temp_password=get_random_string(8)
                user.set_password(temp_password)
                user.save()
                profile=user.studentprofile
                profile.is_temp_password=True
                profile.save()

                send_mail(
                    'Your Temporary Password', f'Here is your temporary password:{temp_password}','vishnuprakash8138@gmail.com',[email],)
                messages.success(request,'A temporary password send to your email.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request,'No account found with that email.')
    else:
            form=ForgotPasswordForm()
    return render(request,'myapp/forgot_password.html',{'form':form})

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('login')  # or handle it as needed

    return render(request, 'myapp/studentdashboard.html', {'student':student})                


@login_required
def course_signup_view(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = CourseSignupForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Course selection updated.")
            return redirect('dashboard_view')
    else:
        form = CourseSignupForm(instance=student)

    return render(request, 'myapp/course_signup.html',{'form':form})





@login_required
def profile_edit_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return HttpResponse("Student profile not found.")

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard_view')
    else:
        form = ProfileEditForm(instance=student)

    return render(request, 'myapp/profile_edit.html',{'form':form}) 