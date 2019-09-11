import os
import random
import time
import jwt

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
# from useraccounts.models import Users
from django.contrib.auth import get_user_model
Users = get_user_model()

# To import JWT settings from project "settings.py" file
from django.conf import settings
JWT_AUTH=settings.JWT_AUTH

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models import ActivationToken,PasswordResetToken

from .send_email import activation_email, password_reset_email

# To register new user
@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    """
    Input should be in the format:
    {"email": "abc@gmail.com", "password": "1234abcd", "confirm_password": "1234abcd"}
    """
    try:
        email = request.data['email']
        password = request.data['password']
        confirm_password = request.data['confirm_password']

        # check if password match
        if password == confirm_password:
            # check email
            if Users.objects.filter(email=email).exists():
                res = {
                    'error': 'User already has a registered account'}
            else:
                user = Users(email=email, password=make_password(confirm_password))
                try:
                    #full_clean method will check if the email is of valid format or not
                    user.full_clean()
                    user.save()
                    activation_email(request, email, user)
                    res = {
                    'success': 'User has been registered successfully'}
                except ValidationError:
                    res = {
                    'error': 'Email field is invalid.'}
        else:
            res = {
                'error': 'Passwords do not match.'}
    except KeyError:
        res = {
            'error': 'Fields missing.'}
    return Response(res, status=status.HTTP_200_OK)


# To activate new user using email verification
@api_view(['GET'])
@permission_classes([AllowAny, ])
def activate(request, uid, token):
    try:
        jwt.decode(token, JWT_AUTH['JWT_SECRET'], algorithm=JWT_AUTH['JWT_ALGORITHM'])
        try:
            db = ActivationToken.objects.get(owner_id=int(uid))
            token_db = db.activation_token
            expiry_at = db.expiry_at
            #check if tokens are equal
            if token_db == token:
                #check for expiry
                if round(time.time()) < int(expiry_at):
                    #update the usertable
                    user =  Users.objects.get(id=uid)
                    user.email_verified = True
                    user.save()
                    #delete the token after verification
                    db.delete()    
                    context = {'result': 'success',}
                else:
                    context = {'result': 'error',}
            else:
                context = {'result': 'error',}

        except (ActivationToken.DoesNotExist, ValueError):
            context = {'result': 'error',}
    except jwt.DecodeError:
        context = {'result': 'error',}

    return render(request, 'activate.html', context)


# To send reset-password link to user
@api_view(['POST'])
@permission_classes([AllowAny, ])
def password_reset(request):
    """
    Input should be in the format:
    {"email": "abc@gmail.com"}
    """
    try:
        email = request.data['email']
        if Users.objects.filter(email=email).exists():
            password_reset_email(request, email, Users.objects.get(email=email))
            res = {
                'success': 'Password reset email sent.'}
        else:
            res = {
                'error': 'Unregistered user account.'}

    except KeyError:
        res = {
            'error': 'Fields missing.'}
    return Response(res, status=status.HTTP_200_OK)


# To handle user password reset link and update the password
@api_view(['GET','POST'])
@permission_classes([AllowAny, ])
def reset(request, uid, token):
    try:
        jwt.decode(token, JWT_AUTH['JWT_SECRET'], algorithm=JWT_AUTH['JWT_ALGORITHM'])
        try:
            db = PasswordResetToken.objects.get(owner_id=int(uid))
            token_db = db.reset_token
            expiry_at = db.expiry_at
            #check if tokens are equal
            if token_db == token:
                #check for expiry
                if round(time.time()) < int(expiry_at):
                    if request.method == 'GET':
                        #show user password update form
                        context = {'result': 'show-form',}
                    else:
                        password = request.data['password']
                        confirm_password = request.data['confirm_password']
                        #check if both the fields are present
                        if password and confirm_password:
                            if password == confirm_password:
                                # change user password
                                user =  Users.objects.get(id=uid)
                                user.password = make_password(confirm_password)
                                user.save()
                                #delete the token after password change
                                db.delete()
                                context = {'result': 'success-done',}
                            else:
                                context ={'result': 'show-form-nomatch'}
                        else:
                            context = {'result': 'show-form-missing',}
                else:
                    context = {'result': 'error',}
            else:
                context = {'result': 'error',}

        except (PasswordResetToken.DoesNotExist, ValueError):
            context = {'result': 'error',}
        
    except jwt.DecodeError:
        context = {'result': 'error'}

    return render(request, 'pass_reset.html',context)