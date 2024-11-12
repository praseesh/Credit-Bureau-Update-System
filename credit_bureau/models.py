from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True, null=False, blank=False, default='9999999999')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    def save(self, *args, **kwargs):
        # Hash password only if it's new or changed
        # if not self.pk or 'password' in kwargs.get('update_fields', []):
        #     print('the not hashed password',self.password)
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

# class User(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, unique=True)
#     mobile = models.CharField(max_length=15, unique=True)
#     password = models.CharField(max_length=255) 

#     def save(self, *args, **kwargs):       
#         self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)
    
class Question(models.Model):
    text = models.TextField() 
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    score_a = models.IntegerField()  
    score_b = models.IntegerField()  
    score_c = models.IntegerField()  
    score_d = models.IntegerField()  

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'question'

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[(
        'A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')
        ])

    def get_score(self):
        if self.selected_option == 'A':
            return self.question.score_a
        elif self.selected_option == 'B':
            return self.question.score_b
        elif self.selected_option == 'C':
            return self.question.score_c
        elif self.selected_option == 'D':
            return self.question.score_d
        return 0
    class Meta:
        db_table = 'user_response'