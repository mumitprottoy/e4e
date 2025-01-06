import requests
from utils import secret, constants as const 


def validate_full_name(first_name: str, last_name: str) -> bool:
    return bool(first_name and last_name)


def generate_email_data(
    email_list: list, operation: str, context: dict, subject_code: str) -> dict:
    return {
        'key': secret.key,
        'kwargs': {
            'recipient_list': email_list,
            'operation': operation,
            'context': context,
            'subject_code': subject_code
        }
    }
    

def send_email_request_to_server(data: dict):
    requests.post(const.code_sending_endpoint, json=data)