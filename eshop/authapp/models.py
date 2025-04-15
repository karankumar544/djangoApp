from django.db import models

# Create your models here.


# class UserAccount(models.Model):
#     user_id = models.ForeignKey()
#     user_email = models.EmailField(verbose_name="email")
#     user_billing = models.TextField()


# class UserProfile(models.Model):
#     user_account = models.ForeignKey(UserAccount)
#     name = models.CharField(default="", name="user_name")
#     father_name = models.CharField(max_length=255)
#     mother_name = models.CharField(max_length=255)
#     profile_image = models.ImageField(upload_to="Profile")
#     is_maraised = models.BooleanField(default=False)
#     age = models.DateTimeField(auto_now_add=True)
