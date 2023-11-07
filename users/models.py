from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User 
import uuid


def generate_profile_id():
    unique_id = uuid.uuid4().hex[:8]  # Generate a random unique ID
    return unique_id



class profile_personal_info(models.Model):   
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
    
    class Diet(models.TextChoices):
        VEG = 'veg', 'Vegetarian'
        NONVEG = 'nonveg', 'Non-Vegetarian'
        EGGTERIAN='eggterian','eggterian'
    class BloodGroup(models.TextChoices):
        A_POSITIVE = 'A+', 'A+'
        A_NEGATIVE = 'A-', 'A-'
        B_POSITIVE = 'B+', 'B+'
        B_NEGATIVE = 'B-', 'B-'
        AB_POSITIVE = 'AB+', 'AB+'
        AB_NEGATIVE = 'AB-', 'AB-'
        O_POSITIVE = 'O+', 'O+'
        O_NEGATIVE = 'O-', 'O-'
    class phd(models.TextChoices):
        NO='none','no'
        YES='yes','yes'
    class Colour(models.TextChoices):
        FAIR = 'fair', 'Fair'
        WHEATISH = 'wheatish', 'Wheatish'
        TANNED = 'tanned', 'Tanned'
        DARK = 'dark', 'Dark'
        BLACK = 'black', 'Black'
        OTHER = 'other', 'Other'
    class MaritalStatus(models.TextChoices):
        NEVERMARRIED = 'Single', 'Single'
        MARRIED = 'Married', 'Married'
        DIVORCED = 'Divorced', 'Divorced'
        WIDOWED = 'Widowed', 'Widowed'
        SEPARATED = 'Separated', 'Separated'

    
    user=models.OneToOneField(User,on_delete=models.CASCADE)   
    profile_id = models.CharField(max_length=10, unique=True, editable=False) 
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    image_pic=models.ImageField(default='default.jpg',upload_to='profile_pics')
    image1=models.ImageField(default='default.jpg',upload_to='profile_pics')
    image2=models.ImageField(default='default.jpg',upload_to='profile_pics')
    image3=models.ImageField(default='default.jpg',upload_to='profile_pics')
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    dob = models.DateField()    
    height = models.FloatField()
    diet = models.CharField(max_length=15, choices=Diet.choices, default=Diet.VEG)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    weigth=models.IntegerField()
    blood_group = models.CharField(max_length=4, choices=BloodGroup.choices, default=BloodGroup.A_POSITIVE)   
    physical_disability=models.CharField(max_length=10,choices=phd.choices,default=phd.NO)
    skin_colour = models.CharField(max_length=10, choices=Colour.choices,default=Colour.FAIR)
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices,default=MaritalStatus.NEVERMARRIED)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number=models.CharField(max_length=13,default='')
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    
    
    def save(self, *args, **kwargs):
        if not self.profile_id:
            self.profile_id = generate_profile_id()
        super(profile_personal_info, self).save(*args, **kwargs)
    
    def _str_(self):
        return f'{self.user.username} profile'

# Create your models here.
class profile_family_details(models.Model):
    profile_id=models.OneToOneField(profile_personal_info,on_delete=models.CASCADE)
    fathers_occupation=models.CharField(max_length=30)
    mothers_occupation=models.CharField(max_length=20)
    religion=models.CharField(max_length=20)
    caste=models.CharField(max_length=20)
    mothertounge=models.CharField(max_length=20)
    
    def _str_(self):
        return f'{self.profile_id.user.username} family details' 
    
class profile_educational_and_career_info(models.Model):
    profile_id=models.OneToOneField(profile_personal_info,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=50)
    collage_name=models.CharField(max_length=50)
    occupation=models.CharField(max_length=50)
    company_name=models.CharField(max_length=50)
    income=models.IntegerField()
    
    def _str_(self):
        return f'{self.profile_id.user.username} educational and carrer info'
    
    
class partner_preferences(models.Model):
    class MaritalStatus(models.TextChoices):
        NEVERMARRIED = 'Single', 'Single'
        MARRIED = 'Married', 'Married'
        DIVORCED = 'Divorced', 'Divorced'
        WIDOWED = 'Widowed', 'Widowed'
        SEPARATED = 'Separated', 'Separated'
    
    
    profile_id=models.OneToOneField(profile_personal_info,on_delete=models.CASCADE)
    agemin=models.IntegerField()
    agemax=models.IntegerField()
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices,default=MaritalStatus.NEVERMARRIED)
    height=models.IntegerField()
    religion=models.CharField(max_length=20)
    caste=models.CharField(max_length=20)
    mothertounge=models.CharField(max_length=20)
    qualificaton=models.CharField(max_length=50)
    occupation=models.CharField(max_length=50)
    income=models.IntegerField()
    country=models.CharField(max_length=20)
    
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics',null=True, blank=True)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    occupation=models.CharField(max_length=50)
    religion=models.CharField(max_length=20)
    caste=models.CharField(max_length=20)
    no=models.IntegerField(null=True,blank=True)
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')