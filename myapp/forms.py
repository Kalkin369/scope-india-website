# forms.py

from django import forms
from .models import Contact
from .models import Student
from .models import StudentProfile



class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','subject','message']

class LoginForm(forms.Form):
   email=forms.EmailField() 
   password=forms.CharField(widget=forms.PasswordInput)
   keep_logged_in=forms.BooleanField(required=False) 


class ForgotPasswordForm(forms.Form):
    email= forms.EmailField()   

class CourseSignupForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['course']
        widgets={'course':forms.Select(attrs={'class':'form-control'})}    



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'full_name', 'date_of_birth', 'gender', 'qualification', 'mobile_number', 'email',
            'guardian_name', 'guardian_occupation', 'guardians_mobile', 'course', 'training_mode',
            'training_location', 'preferred_timings', 'address', 'country', 'state', 'city', 'zip_code'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'training_mode': forms.RadioSelect(choices=[('Online', 'Live online'), ('Offline', 'Classroom')]),
            'training_location': forms.RadioSelect(choices=[
                ('Technopark TVM', 'Technopark TVM'),
                ('Thampanoor TVM', 'Thampanoor TVM'),
                ('Kochi', 'Kochi'),
                ('Nagercoil', 'Nagercoil'),
                ('Online', 'Online')
            ]),
            'preferred_timings': forms.Select(choices=[
                ('Between 8am - 10am', 'Between 8am - 10am'),
                ('Between 9am - 1pm', 'Between 9am - 1pm'),
                ('Between 1pm - 6pm', 'Between 1pm - 6pm'),
                ('Between 6pm - 10pm', 'Between 6pm - 10pm')
            ]),
            'course': forms.Select(choices=[(c, c) for c in Student.COURSE_CHOICES]),
}
