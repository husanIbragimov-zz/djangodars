from django.urls import path
from .views import (home_view,
                    article_detail_view,
                    search_article_view,
                    create_article_view,
                    article_create_form_view,
                    my_articles_view,
                    article_update_view
                    )


urlpatterns = [
    path('', home_view),
    # path('<int:year>/<int:month>/<int:day>/<slug:slug>/', article_detail_view),
    path('search/', search_article_view),
    path('my-articles/', my_articles_view),
    path('create/', create_article_view),
    path('fcreate/', article_create_form_view, name='fcreate'),
    path('<slug:slug>/', article_detail_view, name='article_detail_view'),
    path('update/<slug:slug>/', article_update_view, name='article_update_view'),

]
