"""payment_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from users.views import Signup, Signin, Transfer, Deposit, Balance, Payment_Order, Payment_Information, Statement, Payment_Check, Payment_Return

urlpatterns = [
    path('admin/', admin.site.urls),
path('Payment_WH/signup/', Signup),
    path('Payment_WH/signin/', Signin),
    path('Payment_WH/deposit/', Deposit),
    path('Payment_WH/balance/', Balance),
    path('Payment_WH/transfer/', Transfer),
    path('Payment_WH/statement/', Statement),
    path('Payment_WH/Payment Order/', Payment_Order),
    path('Payment_WH/Payment Information/', Payment_Information),
    path('Payment_WH/Payment Check/', Payment_Check),
    path('Payment_WH/Payment Return/', Payment_Return),
]
