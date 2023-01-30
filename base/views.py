from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import foodlist, foodlike, User
from base.serilizer import foodlistserializer, foodlikeserializer


@api_view(['GET'])
def home(request):
    foo = foodlist.objects.all()
    if foo:
        serializer = foodlistserializer(foo, many=True)
        return Response(serializer.data)
    else:
        context = {'empty:', 'No Items found'}
        return Response(context)


@api_view(['GET'])
def singlefood(request, pk):
    auth = authenticate(username=request.session.get('email'), password=request.session.get('password'))
    if auth:
        foo = foodlist.objects.get(id=pk)
        serializer = foodlistserializer(foo, many=False)
        return Response(serializer.data)
    else:
        context = {'error': 'User credential are not correct'}
        return Response(context)


@api_view(['GET'])
def logins(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    auth = authenticate(username=email, password=password)
    if auth:
        context = {'success': 'successful login'}
        request.session['email'] = email
        request.session['password'] = password

        return Response(context)
    else:
        context = {'error': 'User name and password are not correct'}

        return Response(context)


@api_view(['GET'])
def logouts(request):
    request.session['email'] = ''
    request.session['password'] = ''
    context = {'success': 'you have successfully logout'}
    return Response(context)


@api_view(['GET'])
def like(request, pk):
    auth = authenticate(username=request.session.get('email'), password=request.session.get('password'))
    if auth:

        foo = User.objects.get(email=request.session.get('email'))
        fooo = foodlist.objects.get(id=pk)
        try:
            li = foo.foodlike_set.get(foodlikeid=fooo.id)
        except:
            li = foo.foodlike_set.create(foodlikeid=str(fooo.id), name=fooo.name, price=fooo.price,
                                         description=fooo.description,
                                         image=fooo.image)
            li.save()
            context = {'success': 'Item liked successfully'}
            return Response(context)

        dell = foo.foodlike_set.get(foodlikeid=fooo.id)
        dell.delete()
        context = {'unlike': 'Item Unliked successfully'}
        return Response(context)


    else:
        context = {'error': 'user credentials are not correct'}
        return Response(context)


# food list loves by the user
@api_view(['GET'])
def crateAccount(request):
    email = request.GET.get('email')
    username = request.GET.get('username')
    city = request.GET.get('city')
    state = request.GET.get('state')
    password = request.GET.get('password')

    confirm_password = request.GET.get('confirm_password')
    if password == confirm_password:
        try:
            us = User.objects.get(email=email)
        except:
            passwords = make_password(password)
            us = User(username=username, email=email, password=passwords, city=city, state=state)
            request.session['email'] = email
            request.session['password'] = password
            us.save()
            context = {'success': 'Account created successfully'}
            return Response(context)
        context = {'error': 'User Already exist'}
        return Response(context)
    else:
        context = {'error': 'password doesnt match'}
        return Response(context)


@api_view(['GET'])
def itemlikedbyuser(request):
    auth = authenticate(username=request.session.get('email'), password=request.session.get('password'))
    if auth:
        foo = User.objects.get(email=request.session.get('email'))

        foodlikes = foo.foodlike_set.all()
        serializer = foodlikeserializer(foodlikes, many=True)
        return Response(serializer.data)
    else:
        context = {'error', 'User credentials is not correct'}
        return Response(context)
