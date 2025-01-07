import random
from django.db import models
from django.contrib.auth.models import User
from stuff import models as stuff_models
from utils.keygen import KeyGen
from . import operations as ops


class Picture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pic')
    url = models.TextField(default='')
    
    def choose_pic(self) -> stuff_models.ProfilePictureURL:
        urls = list(stuff_models.ProfilePictureURL.objects.all())
        return random.choice(urls)
    
    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.choose_pic().url
        super().save(*args, **kwargs)


class Phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone')
    number = models.CharField(max_length=20, default='') 
    
    def __str__(self):
        return f'{self.user.email} : {self.number}'
    
        
class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')
    is_premium = models.BooleanField(default=False)
    
    @property
    def is_sales_partner(self):
        return hasattr(self.user, 'partner')
    
    def update_to_premium(self):
        self.is_premium = True
        self.save()
    
    def __str__(self):
        status = 'Premium' if self.is_premium else 'Ordinary'
        return f'{self.user.email} : {status}'
    

class SixDigitCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='codes')
    otp = models.CharField(max_length=6, default='') 
    verification_code = models.CharField(max_length=6, default='')
    is_verified = models.BooleanField(default=False)
    
    def __generate_code(self):
        return KeyGen().num_key()
    
    def change_otp(self):
        self.otp = self.__generate_code()
        self.save()
    
    def change_verification_code(self):
        self.verification_code = self.__generate_code()
        self.save()
    
    def send_code(self, code_type: str):
        operation = 'reset_password' if code_type == 'OTP' else 'verify_email'
        context = {
            'code_type': code_type, 'code': self.otp if code_type == 'OTP' else self.verification_code}
        data = ops.generate_email_data([self.user.email], operation, context, context['code'])
        ops.send_email_request_to_server(data)
    
    def send_otp(self):
        self.send_code('OTP')
    
    def send_verification_code(self):
        self.send_code('verification code')
        
    def verify_email(self):
        self.is_verified = True
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.__generate_code()
        if not self.verification_code:
            self.verification_code = self.__generate_code()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.user.email