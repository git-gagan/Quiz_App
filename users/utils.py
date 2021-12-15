from django.core.mail import send_mail
#from quizproject.settings import EMAIL_HOST_USER


def mail(email, otp):
    sender = 'er.gaganraj@gmail.com'
    receiver = email
    message = f"""
                From: From {sender}
                #To: To {receiver}
                Hey Buddy, 
                Thanks for signing up. Your OTP is {otp}.
                It is valid for 1 minute. Be quick!
                """
    send_mail(
        'OTP verification',
        message,
        sender,
        [receiver],
        fail_silently=False,
    )