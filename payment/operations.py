from . import constants as const 


def resolve_trx_check_url(trx: str):
    return f"https://secure.aamarpay.com/api/v1/trxcheck/request.php?request_id={trx}&store_id={const.store_id}&signature_key={const.signature_key}&type=json"


def payment_status(trx: str) -> bool:
    from requests import get
    try:
        response = get(resolve_trx_check_url(trx=trx)).json()
        return ('pay_status' in response) and (response['pay_status'] == 'Successful')
    except: return False

      