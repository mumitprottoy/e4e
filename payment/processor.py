from datetime import datetime
from .payload import get_payload
from django.contrib.auth.models import User
from sales.models import Channel
from . import models



class PaymentProcessor:

    def __init__(self, user: User, key = str()) -> None:
        self.user = user
        self.key = key

    def get_channel(self) -> Channel | None:
        channel_bulk = Channel.objects.filter(key=self.key)
        if channel_bulk.exists():
            return channel_bulk.first()
        return Channel.get_default()
        
    def initiate_purchaseV3(self) -> models.PurchaseV3:
        channel = self.get_channel()
        purchaseV3 = models.PurchaseV3.objects.filter(user=self.user)
        if purchaseV3.exists(): 
            purchaseV3 = purchaseV3.first()
            if not purchaseV3.pending_payment_is_done:
                purchaseV3.set_new_channel(channel)
            return purchaseV3
        else: 
            purchaseV3 = models.PurchaseV3(user=self.user, channel=channel)
            purchaseV3.save()
            return purchaseV3
            
    
    def request_gateway(self, purchaseV3: models.PurchaseV3):
        # purchaseV3 = self.initiate_purchaseV3()
        if purchaseV3 is not None:
            if not purchaseV3.is_closed:
                if purchaseV3.has_attempted and purchaseV3.window_is_closed:
                    return None
                purchaseV3.update_transaction_id()
                purchaseV3.issued_at = datetime.now()
                purchaseV3.save()
                payload = get_payload(purchaseV3)
                from aamarpay.aamarpay import aamarPay
                print(payload)
                _ = aamarPay(**payload)
                return _.payment()
