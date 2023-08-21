from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserRegisterSerializer, MovieSerializer,BookingSerializer
from rest_framework import generics
from .models import UserDetails, MovieDetails, MovieBooking
import json , requests
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import serializers


class MySerialize(serializers.Serializer):
    Moviename= serializers.CharField()
    Movietype = serializers.CharField()

    def validate_Moviename(self, value):
        if not value:
            raise serializers.ValidationError('Enter the movie name')
        return value
        
    def validate_MovieType(self, value):
        if not value:
            raise serializers.ValidationError("Enter the movie type")
        return value


class PaySerialize(serializers.Serializer):
    Movieprice = serializers.CharField()
    Quantity = serializers.IntegerField()
    MovieID = serializers.IntegerField()
    UserID = serializers.IntegerField()

    def validate_MovieID(self, value):
        if not value:
            raise serializers.ValidationError('Enter the movie id')
        return value

    def validate_Movieprice(self, value):
        if not value:
            raise serializers.ValidationError('Enter the movie price')
        return value
    
    def validate_Quantity(self, value):
        if not value:
            raise serializers.ValidationError("Enter the quantity")
        return value
    
    def validate_UserID(self, value):
        if not value:
            raise serializers.ValidationError("Enter your ID")
        return value


@api_view(['GET', 'POST'])
def validate(request):
    request_object=json.loads(request.body)
    return_object= {"details":request_object['name']}
    return JsonResponse(return_object,safe=False)

def register_user(request):
    request_object=json.loads(request.body)
    queryset = UserDetails()
    user_exist=UserDetails.objects.filter(email_id= request_object['email_id']).exists()
    if user_exist==False:
        queryset.Username= request_object['Username']
        queryset.email_id= request_object['email_id']
        queryset.password= request_object['password']
        repeat = queryset.save()
        return_object= {"message":"user added successfully"}
        return JsonResponse(return_object,safe=False)
    else:
        return JsonResponse({"messsage":"user already exist"})

def validate_user(request,pk=None):
    request_object=json.loads(request.body)
    user_details=UserDetails.objects.filter(UserID= request_object['UserID'])
    user_password=UserDetails.objects.filter(password= request_object['password']).exists()
    if user_details and request.method=='POST':
        if user_password==True:
            id=pk
            if id is not None:
                movie = MovieDetails.objects.filter(MovieID=id)
                serializer = MovieSerializer(movie, many=True)
                print(serializer.data)
                return JsonResponse(serializer.data,safe=False)
            movie=MovieDetails.objects.all()
            serializer = MovieSerializer(movie, many=True)
            print(serializer.data)
            return JsonResponse(serializer.data,safe=False)
        else:
            return_object={"message":"Invalid Password"}
    else:
        return_object= {"message":"Invalid credentials"}
    return JsonResponse(return_object,safe=False)


def movie_list(request):
    request_object=json.loads(request.body)
    queryset = MovieDetails()
    queryset.Moviename= request_object['Moviename']
    queryset.Movietype= request_object['Movietype']
    queryset.Movieprice= request_object['Movieprice']
    queryset.save()
    return_object= {"message":"Movie added successfully"}
    return JsonResponse(return_object,safe=False)


@api_view(['GET', 'POST'])
def get_movie(request):
    if request.method=='GET':
        movie=MovieDetails.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        post_data = json.loads(request.body)
        serializer = MySerialize(data=post_data)
        if serializer.is_valid():
            MovieDetails.objects.create(**post_data)
            return JsonResponse({
            'message': 'Data stored'
        })
        print(json.loads(request.body))
        return JsonResponse({
            'message': 'Data not stored'
        })


@api_view(['POST'])
def book_movie(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print(post_data,"@@@@@@@@@@")
        id = post_data['MovieID']
        print(id)
        quantity = post_data['Quantity']
        price_movie = post_data['Movieprice']
        serial = PaySerialize(data=post_data)

        if serial.is_valid():
            user = UserDetails.objects.filter(UserID=request.body['UserID']).exists()
            print(user,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            get_movie = MovieDetails.objects.filter(MovieID=id)
            serializer = list(get_movie.values())
            calculated_price = int(serializer[0]['Movieprice']) * int(quantity)
            
            if calculated_price == int(price_movie):
                MovieBooking.objects.create(**serial.validated_data)
                return JsonResponse({
                    'Message': 'Ticket has been booked'
                })
        else: 
            return JsonResponse({
                'error': serial.errors,
            })
        return JsonResponse({
            'message': 'Inappropriate Amount',
        })
    
        
        


