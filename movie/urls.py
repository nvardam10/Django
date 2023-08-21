from django.urls import path
from .views import *
urlpatterns = [
    path('register',UserRegisterView.as_view()),
    path('register/<int:UserID>/', UserDetailedView.as_view()),

    path('login',UserLoginView.as_view()),
    path('login/<int:pk>/',UserLoginView.as_view()),

    path('list',MovieListView.as_view()),
    path('list/<int:MovieID>/', MovieDetailedView.as_view()),

    path('booking',BookingView.as_view()),
    path('booking/<int:BookingID>/', BookingDetailedView.as_view()),

]