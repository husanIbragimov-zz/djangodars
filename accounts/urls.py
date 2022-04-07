from django.urls import path
from .views import (login_view,
                    logout_view,
                    user_register_view,
                    index_view,)

urlpatterns = [
    path('', index_view, name='index_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('register/', user_register_view, name='user_register_view'),
]