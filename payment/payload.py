from . import constants as const 
from . import models


def get_payload(purchase: models.PurchaseV3) -> dict:
    payload = {
        "isSandbox" : False,
        "storeID" : const.store_id,
        # "successUrl" : const.return_url+purchase.tracker.key,
        # "failUrl" : const.return_url+purchase.tracker.key,
        # "cancelUrl" : const.return_url+purchase.tracker.key,
        "successUrl" : const.return_url,
        "failUrl" : const.return_url,
        "cancelUrl" : const.return_url,
        "transactionID" : purchase.transaction_id,
        "transactionAmount" : str(float(purchase.payable_amount)),
        "signature" : const.signature_key,
        "customerState" : str(purchase.tracker.id),
        "customerName" : purchase.user.get_full_name(),
        "customerEmail" : purchase.user.email,
        "customerMobile" : purchase.user.phone.number if hasattr(purchase.user, 'phone') else '018768815107'
    }

    return payload