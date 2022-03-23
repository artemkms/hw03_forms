from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),  # 1
    path('', include('posts.urls', namespace='posts')),  # 2
    path('group/<slug:slug>/', include('posts.urls', namespace='posts')),  # 3
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]


# Если переставить "второй" и "третий" местами -
# джанго начнет передавать slug в index()
# не до конца понимаю как это всё работает,
# но если ничего не менять - всё работает :)
# https://ibb.co/Y3rL3HN <- то, что получается
# https://ibb.co/8zMYxZs <- работает
