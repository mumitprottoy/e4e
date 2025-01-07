from datetime import datetime
from django.core import exceptions
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from productmanagement.models import Product
from sales.models import Channel
from utils import keygen
from . import operations as ops


class PaymentTracker(models.Model):
    key = models.CharField(max_length=200, unique=True, default='')
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = keygen.KeyGen().alphanumeric_key(100)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.key


class PurchaseV3(models.Model):
    tracker = models.OneToOneField(PaymentTracker, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    transaction_id = models.CharField(max_length=200, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    is_closed = models.BooleanField(default=False)
    issued_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    attempt_count = models.IntegerField(default=-1)
    
    def __generate_transaction_id(self):
        return keygen.KeyGen().transaction_id()
    
    def update_transaction_id(self):
        self.transaction_id = self.__generate_transaction_id()
        self.save()
    
    def update_key(self, key:str):
        self.key = key
        self.save()
        
    def set_new_channel(self, channel: Channel):
        self.channel = channel
        self.save()
    
    @property
    def pending_payment_is_done(self):
        return ops.payment_status(self.transaction_id)
    
    @classmethod
    def initiate_transaction(cls, user: User, key: str):
        pass
            
    @property
    def has_attempted(self):
        return self.attempt_count > 0 

    @property
    def payable_amount(self):
        payable = self.product.price - self.channel.deductible_amount
        return payable if payable > 0 else 0
    
    @property
    def is_payable(self):
        return self.payable_amount > 0
    
    @property
    def time_passed(self):
        return (datetime.now().astimezone(tz=timezone.get_current_timezone()) - self.issued_at).total_seconds()
    
    @property
    def time_left(self):
        left  = 15*60 - self.time_passed
        return left if left > 0 else 0
    
    @property
    def time_left_json_script(self):
        return f'<script>const secsLeft = {self.time_left};</script>'
    
    @property
    def time_left_in_minutes(self):
        left = self.time_left
        minute = left // 60
    
    @property
    def is_discounted(self):
        return self.payable_amount < self.product.price
    
    def discounted_amount(self):
        amount = self.product.price - self.payable_amount
        return amount if amount > 0 else 0       
    
    @property
    def window_is_closed(self):
        if self.issued_at is not None:
            return self.time_passed < 15*60
        return False
    
    def close_transaction(self):
        if not self.is_closed:
            self.is_closed = True
            self.save()
        else: raise exceptions.ValidationError('Cannot close an already close transaction.')
    
    def save(self, *args, **kwargs):
        self.attempt_count += 1
        if self.tracker is None:
            tracker = PaymentTracker(key=''); tracker.save()
            self.tracker = tracker
        if self.channel is None: self.channel = Channel.get_default()
        if self.product is None: self.product = Product.get_product()
        if not self.transaction_id:
            self.transaction_id = self.__generate_transaction_id()
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'edtech_payment_purchase_v3'


class Payment(models.Model):
    tracker = models.OneToOneField(PaymentTracker, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=200, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    issued_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    attempt_count = models.IntegerField(default=-1)
    
    def __generate_transaction_id(self):
        return keygen.KeyGen().transaction_id()
    
    def update_transaction_id(self):
        self.transaction_id = self.__generate_transaction_id()
        self.save()
    
    def update_key(self, key:str):
        self.key = key
        self.save()
        
    def set_new_channel(self, channel: Channel):
        self.channel = channel
        self.save()
    
    @property
    def pending_payment_is_done(self):
        return ops.payment_status(self.transaction_id)
    
    @classmethod
    def initiate_transaction(cls, user: User, key: str):
        pass
            
    @property
    def has_attempted(self):
        return self.attempt_count > 0 

    @property
    def payable_amount(self):
        payable = self.product.price - self.channel.deductible_amount
        return payable if payable > 0 else 0
    
    @property
    def is_payable(self):
        return self.payable_amount > 0
    
    @property
    def time_passed(self):
        return (datetime.now() - self.issued_at).total_seconds()
    
    @property
    def window_is_closed(self):
        return self.time_passed < 10*60

    def close_transaction(self):
        if not self.is_closed:
            self.is_closed = True
            self.save()
        else: raise exceptions.ValidationError('Cannot close an already close transaction.')
    
    def save(self, *args, **kwargs):
        if not self.user: self.user = User.objects.first()
        self.product = Product.objects.first()
        self.attempt_count += 1
        if not self.tracker:
            tracker = PaymentTracker(); tracker.save()
            self.tracker = tracker
        if not self.channel: self.channel = Channel.get_default()
        if not self.transaction_id:
            self.transaction_id = self.__generate_transaction_id()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.user.email
    



    
    