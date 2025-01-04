from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    ORG = 'Organic'; ADV = 'Learning Advocate'; GUIDE = 'Learning Guide'; REF = 'Referrer'
    PARTNER_TYPE_CHOICES = ((ORG, ORG), (ADV, ADV), (GUIDE, GUIDE), (REF, REF))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner')
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE_CHOICES)
    coupon_code = models.CharField(max_length=20, unique=True, blank=True, null=True)    
    key = models.CharField(max_length=200, unique=True, blank=True, null=True)
    deductible_amount = models.IntegerField(default=0)
    
    @property
    def not_organic(self):
        return self.partner_type != self.ORG
    
    @classmethod
    def get_default(cls):
        return cls.objects.filter(partner_type=cls.ORG).first()
        
    def __str__(self) -> str:
        return f'{self.user.email} : {self.partner_type}'    
