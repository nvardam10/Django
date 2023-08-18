from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User_Details,Movie_Details,Movie_Booking
from .serializers import UserRegisterSerializer,MovieSerializer,BookingSerializer
import json
import hashlib
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

# def get_object_v1(self, MovieID = 0 ,UserID = 0):        
#         try:
#             print('111111111',MovieID,UserID)
#             if MovieID :
#                 return  Movie_Details.objects.get(pk=MovieID)
#             print('111111111',UserID ,'222222222', MovieID)
#             if UserID:
#                 return  User_Details.objects.get(pk=UserID)
#         except  Movie_Details.DoesNotExist:
#             print('000000000000000')
#             return None
        
class UserRegisterView(APIView):
    def get(self, request):
        users = User_Details.objects.all()
        serializer = UserRegisterSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            # hashed_password = make_password(password)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user = User_Details.objects.create(
                Username=serializer.validated_data['Username'],
                password=hashed_password,
                email_id=serializer.validated_data['email_id'],
                phone=serializer.validated_data['phone'],
            )
            return Response(UserRegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailedView(APIView):
    # def get_object(self,UserID):
    #     return get_object_v1(self,0 ,UserID)
    def get_object(self, UserID):
        try:
            return  User_Details.objects.get(pk=UserID)
        except  User_Details.DoesNotExist:
            return Response({'message': 'No content to show'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, UserID):
        user = self.get_object(UserID)
        if user is None:
            return Response({'message': 'User not registered'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegisterSerializer(user)
        return Response(serializer.data)

    def put(self, request, UserID):
        user = self.get_object(UserID)
        if user is None:
            return Response({'message': 'User not registered'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegisterSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, UserID):
        user = self.get_object(UserID)
        if user is None:
            return Response({'message': 'User not registered'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class UserLoginView(APIView):
    def post(self, request,pk=None):
        request_object=json.loads(request.body)
        user = User_Details.objects.filter(UserID=request_object['UserID']).first()
        # user_details=User_Details.objects.filter(UserID=request_object['UserID'])
        # user_password = user_details.values('password')
        if user is not None:
            
            # if user_password[0]['password'] == request_object['password']:
            # if check_password(request_object['password'], user.password):
            if user.password == hashlib.sha256(request_object['password'].encode()).hexdigest():
                id=pk
                if id is not None:
                    movie=Movie_Details.objects.filter(MovieID=id)
                    serializer = MovieSerializer( movie, many=True)
                    return Response(serializer.data)
                movies =  Movie_Details.objects.all()
                serializer = MovieSerializer( movies, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
                

class MovieListView(APIView):
    def get(self, request):
        movies =  Movie_Details.objects.all()
        serializer = MovieSerializer( movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailedView(APIView):
    def get_object(self, MovieID):
        try:
            return  Movie_Details.objects.get(pk=MovieID)
        except  Movie_Details.DoesNotExist:
            return Response({'message': 'No content to show'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, MovieID):
        movie = self.get_object(MovieID)
        if movie is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer =  MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, MovieID):
        movie = self.get_object(MovieID)
        if movie is None:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, MovieID):
        movie = self.get_object(MovieID)
        if movie is None:
            return Response({'message': 'movie not found'}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response({'message': 'movie deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class BookingView(APIView):
    
    def get(self, request):
        book =  Movie_Booking.objects.all()
        serializer = BookingSerializer( book, many=True)
        return Response(serializer.data)

    def post(self, request):
        request_data = request.data
        id = request_data.get('MovieID')
        quantity = request_data.get('Quantity')
        price_movie = request_data.get('Movieprice')
        serializer = BookingSerializer(data=request_data)
        
        if serializer.is_valid():
            user = User_Details.objects.filter(UserID=request_data.get('UserID')).exists()
            movie = Movie_Details.objects.filter(MovieID=id).exists()
            
            if movie:
                if user:
                    get_movie = Movie_Details.objects.get(MovieID=id)
                    calculated_price = int(get_movie.Movieprice) * int(quantity)
                    
                    if calculated_price == int(price_movie):
                        Movie_Booking.objects.create(**serializer.validated_data)
                        return JsonResponse({
                            'message': 'Ticket has been booked'
                        })
                    else:
                        return JsonResponse({
                            'message': 'Inappropriate Amount'
                        })
                else:
                    return JsonResponse({
                        'error': serializer.errors
                    })
            else:
                return JsonResponse({
                    'error': serializer.errors
                })
        else:
            return JsonResponse({
                'error': serializer.errors
            })



class BookingDetailedView(APIView):
    def get_object(self, BookingID):
        try:
            return  Movie_Booking.objects.get(pk=BookingID)
        except  Movie_Booking.DoesNotExist:
            return Response({'message': 'No content to show'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, BookingID):
        booking = get_object_or_404(Movie_Booking, pk=BookingID,deleted=False)
        user_data = booking.UserID 
        movie_data = booking.MovieID  

        user_serializer = UserRegisterSerializer(user_data)
        movie_serializer = MovieSerializer(movie_data)

        user={ 
            'Username': user_serializer.data['Username'],
            'email_id': user_serializer.data['email_id'],
            'Moviename': movie_serializer.data["Moviename"],
            'quantity': BookingSerializer(booking).data["Quantity"]
        }
        return Response(user)
    

    def put(self, request, BookingID):
        book = get_object_or_404(Movie_Booking, pk=BookingID,deleted=False)
        request_data = request.data
        id = request_data.get('MovieID')
        quantity = request_data.get('Quantity')
        price_movie = request_data.get('Movieprice')
        if book is None:
            return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(book, data=request.data)
        if serializer.is_valid():
            get_movie = Movie_Details.objects.get(MovieID=id)
            calculated_price = int(get_movie.Movieprice) * int(quantity)
            if calculated_price == int(price_movie):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'message': 'Inappropriate Amount'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

    def delete(self, request,  BookingID):
        booking = get_object_or_404(Movie_Booking, pk=BookingID,deleted=False)
        booking.deleted = True
        booking.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # book = self.get_object( BookingID)
        # if book is None:
        #     return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        # book.delete()
        # return Response({'message': 'Booking canceled'}, status=status.HTTP_204_NO_CONTENT)

            # def get(self, request,  BookingID):
    #     book = self.get_object( BookingID)
    #     if book is None:
    #         return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer =  BookingSerializer(book)
    #     return Response(serializer.data)

          # def put(self, request,  BookingID):
    #     book = self.get_object( BookingID)
    #     if book is None:
    #         return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = BookingSerializer(book, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)