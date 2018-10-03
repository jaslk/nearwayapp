"""nearway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.test, name="homepage"),
    path('twtr', views.test_twitter, name="twitter"),
    path('admin/', admin.site.urls),
    path('testing',views.test,name="test"),
    path(r'^export/xls/$', views.export_users_xls, name='export_users_xls'),
]

#  path have 4 arguments:
#  route
#  view
#  kwargs // optional
#  name  // optional
