# models.py

from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=200)
    message=models.TextField()

    def __str__(self):
        return self.name
    




class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    qualification = models.CharField(max_length=40, blank=True)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    guardian_name = models.CharField(max_length=40, blank=True)
    guardian_occupation = models.CharField(max_length=40, blank=True)
    guardians_mobile = models.CharField(max_length=15, blank=True)
    COURSE_CHOICES =[
        ('PHP Full Stack','PHP Full Stack'),
        ('PYTHON Full Stack','PYTHON Full Stack'),
        ('JAVA Full Stack','JAVA Full Stack'),
        ('C#.NET Core 7 Full Stack','C#.NET Core 7 Full Stack'),
        ('MEAN Full Stack','MEAN Full Stack'),
        ('MERN Full Stack','MERN Full Stack'),
        ('Data Science & AI (Python Guru)','Data Science & AI (Python Guru)'),
        ('Python Mastery (Python/Django/MySQL)','Python Mastery (Python/Django/MySQL)'),
        ('Google Flutter Mobile App Development (iOS/Android)','Google Flutter Mobile App Development (iOS/Android)'),
        ('UI/UX Designing','UI/UX Designing'),
        ('Digital Marketing Master Program','Digital Marketing Master Program'),
        ('Software Testing Advanced (Manual/Automation)','Software Testing Advanced (Manual/Automation)'),
        ('Software Testing Manual (ISTQB)','Software Testing Manual (ISTQB)'),
        ('Selenium TestNG & Cucumber/Appium Mobile/QTP/Loadrunner/Jmeter/Jira','Selenium TestNG & Cucumber/Appium Mobile/QTP/Loadrunner/Jmeter/Jira'),
        ('Computer Networking (CCNA)','Computer Networking (CCNA)'),
        ('Server Admin (MCSE)','Server Admin (MCSE)'),
        ('Server Admin (RHCE)','Server Admin (RHCE)'),
        ('Networking & Server Admin (CCNA/MCSE/Hardware)','Networking & Server Admin (CCNA/MCSE/Hardware)'),
        ('Networking & Server Admin (CCNA/RHCE/Hardware)','Networking & Server Admin (CCNA/RHCE/Hardware)'),
        ('Networking & Server Admin (CCNA/MCSE/RHCE/Hardware)','Networking & Server Admin (CCNA/MCSE/RHCE/Hardware)'),
        ('Security Surveillance & Networking Internship (CCNA/CCTV/Hardware)','Security Surveillance & Networking Internship (CCNA/CCTV/Hardware)'),
        ('Cloud Admin (AWS/MS AZURE)','Cloud Admin (AWS/MS AZURE)'),
        ('Cloud & Networking Admin (CCNA/AWS/Hardware)','Cloud & Networking Admin (CCNA/AWS/Hardware)'),
        ('Cloud & Networking Admin (CCNA/MS Azure/Hardware)','Cloud & Networking Admin (CCNA/MS Azure/Hardware)'),
        ('Cloud & Networking Admin (CCNA/AWS)','Cloud & Networking Admin (CCNA/AWS)'),
        ('Cloud & Networking Admin (CCNA/MS Azure)','Cloud & Networking Admin (CCNA/MS Azure)'),
        ('Cloud & Server Admin (MCSE/AWS/Hardware)','Cloud & Server Admin (MCSE/AWS/Hardware)'),
        ('Cloud & Server Admin (MCSE/MS Azure/Hardware)','Cloud & Server Admin (MCSE/MS Azure/Hardware)'),
        ('Cloud & Server Admin (RHCE/AWS/Hardware)','Cloud & Server Admin (RHCE/AWS/Hardware)'),
        ('Cloud & Server Admin (RHCE/MS Azure/Hardware)','Cloud & Server Admin (RHCE/MS Azure/Hardware)'),
        ('Cloud, Networking, & Server Admin (CCNA/AWS/AZURE/MCSE/RHCE/Hardware)','Cloud, Networking, & Server Admin (CCNA/AWS/AZURE/MCSE/RHCE/Hardware)'),
        ('DevOps Mastery (All together)','DevOps Mastery (All together)'),
        ('DevOps - Selective','DevOps - Selective'),
        ('Academic Project','Academic Project'),
        ('MS Office (Word/Excel/Power Point/Outlook)','MS Office (Word/Excel/Power Point/Outlook)'),
        ('Data Analytics','Data Analytics'),
        ('Advanced MS Excel','Advanced MS Excel'),
        ('Graphic Designing (Photoshop)','Graphic Designing (Photoshop)'),
        ('Graphic Designing (Photoshop/Illustrator)','Graphic Designing (Photoshop/Illustrator)'),
        ('None of the above, will discuss directly','None of the above, will discuss directly'),
        
    ]
    course = models.CharField(max_length=300, choices=COURSE_CHOICES) # Store comma-separated values
    TRAINING_MODE_CHOICES = [('Online', 'Online'), ('Offline', 'Offline')]
    training_mode = models.CharField(max_length=20,choices=TRAINING_MODE_CHOICES)  # Online or Offline
    LOCATION_CHOICES = [
        ('Technopark TVM', 'Technopark TVM'),
        ('Thampanoor TVM', 'Thampanoor TVM'),
        ('Kochi', 'Kochi'),
        ('Nagercoil', 'Nagercoil'),
        ('Online', 'Online')
    ]
    training_location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    TIMING_CHOICES = [
        ('Between 8am - 10am', 'Between 8am - 10am'),
        ('Between 9am - 1pm', 'Between 9am - 1pm'),
        ('Between 1pm - 6pm', 'Between 1pm - 6pm'),
        ('Between 6pm - 10pm', 'Between 6pm - 10pm')
    ]

    preferred_timings = models.CharField(max_length=200,choices=TIMING_CHOICES)  # Comma-separated checkboxes

    address = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # def get_course_list(self):
    #     return [c.strip() for c in self.course.split(',') if c.strip()]

    # def get_timings_list(self):
    #     return [t.strip() for t in self.preferred_timings.split(',') if t.strip()]

    def __str__(self):
        return self.full_name
    
class Course(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField(unique=True,blank=True)
    category=models.CharField(max_length=100)
    description=models.TextField()
    duration=models.CharField(max_length=100,blank=True)
    fees=models.CharField(max_length=100,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name  
            
class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_temp_password=models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
  
