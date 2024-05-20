from pydantic import EmailStr
from django.utils.text import slugify
from typing import Union
import re
from django.contrib.auth.hashers import check_password,make_password 
from datetime import datetime,timedelta
from django.conf import settings
from django.db.models import Model
import jwt
from django.core.mail import send_mail

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def checkEmailExisted(email:EmailStr)->bool:
    from authentication.models import Users
    if Users.objects.filter(email = email).exists():
        return True
    else:
        return False
    
def createUserName(email:EmailStr)->str:
    resultSplited = email.split("@")
    result = resultSplited[0]
    if checkEmailExisted(email):
        result = slugify(resultSplited[0]+resultSplited[1])
    else:
        result = slugify(result)
    return result

def createHashedPassword(password : str )->str:
    return make_password(password)

def createForgetPasswordToken(user : object)->str:
    dt = datetime.now() + timedelta(minutes=15)
    tokenValue = {
        "id": 366,
        "email":user.email,
        'exp': int(dt.timestamp())
    }
    token = jwt.encode(tokenValue, settings.SECRET_KEY, algorithm='HS256')
    return token 

def sendForgetMail(user : object)->str:
    token = createForgetPasswordToken(user)
    try:
        a = send_mail(
            subject="Forget password mail ",
            message=f"{settings.BASE_URL}/auth/verifyFToken/?{token}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
    except:
        pass # TODO remove when you configure smtp 
    return token

def decodeJwt(token:str)->tuple:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return (
            True,
            {
                "email" : payload.get("email"),
            }
            ) 
    except:
        msg = 'Invalid authentication. Could not decode token.'
        return (False,{"error":msg})
