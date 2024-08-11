import logging

from celery import shared_task

logging.basicConfig(level=logging.INFO)


@shared_task
def send_sms_task(*, cellphone: str, message: str):
    # Here you would implement the actual SMS sending logic.
    # For the purpose of this example, we simulate it with a logging statement.
    logging.info(f"Sending SMS to {cellphone} with OTP: {message}")
    # In real implementation, you would use the SMS gateway API here.
    # Example:
    # sms_service.send_sms(cellphone=cellphone, message=f"Your OTP is {otp}")
