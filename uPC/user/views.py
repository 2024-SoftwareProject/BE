import json, bcrypt, jwt, re

from django.views   import View
from django.http    import JsonResponse, HttpResponse
from django.shortcuts import render

from .models        import User
from private_settings   import SECRET_KEY, ALGORITHM
# Create your views here.

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']


            # 존재하는 메일이라면
            if User.objects.filter(email=email).exists():
                    return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 400)


            # email, password 조건
            regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '\S{8,25}'
            
            if not re.match(regex_email, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
            if not re.match(regex_password, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)


            # password 인코딩
            password = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')


            User.objects.create(email=email, password=password_crypt)
            return JsonResponse({'message': 'SUCCESS!'}, status=201)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

