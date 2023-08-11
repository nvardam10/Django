from django.urls import path
from .views import *
urlpatterns = [
    # path('register/', Register.as_view()),
    path('register-user',register_user),
    path('validate-user',validate_user),
    path('validate-user/<int:pk>/',validate_user),
    path('movie',movie_list),
    path('movies',get_movie),
    path('booking',book_movie)



]