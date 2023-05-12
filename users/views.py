from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import User, Bill
from .serializers import UserSerializer
import json
from datetime import datetime
import secrets


# Create your views here.
# Sign up new user
def Signup(request):
    if request.method == "POST":
        signup_user = json.loads(request.body)
        signup_username = signup_user["username"]
        signup_password = signup_user["password"]
        signup_deposit = 500
        signup_name = signup_user["name"]
        check_existence = User.objects.filter(username=signup_username)
        if len(check_existence) != 0:
            return JsonResponse({"msg": "The username already exists. Please change the name."})
        signup_User = User(username=signup_username, password=signup_password, deposit=signup_deposit,
                           name=signup_name)
        signup_User.save()
        return JsonResponse({"msg": signup_User.id})


def Signin(request):
    if request.method == "POST":
        signin_user = json.loads(request.body)
        signin_username = signin_user["username"]
        signin_password = signin_user["password"]
        search_user = User.objects.filter(username=signin_username).first()
        if search_user is None:
            return JsonResponse({"msg": "The account does not exist. Please check the information or sign up first."})
        check_password = search_user.password
        if check_password == signin_password:
            return JsonResponse({"msg": search_user.id})
        else:
            return JsonResponse({"msg": "Invalid password."})


def Deposit(request):
    if request.method == "POST":
        ask_user = json.loads(request.body)
        user_Id = ask_user["uid"]
        payment_user = User.objects.filter(id=user_Id).first()
        return JsonResponse({"msg": payment_user.deposit})

def Payment_Information(request):
    if request.method == 'POST':
        airline_order = None
        money = None
        airline_name = None
        data = json.loads(request.body)
        ticket = data.get("order_id") and data.get("seat_price") and data.get("air_name") and len(data) == 3
        if ticket:
            airline_order = data["order_id"]
            money = data["seat_price"]
            airline_name = data["air_name"]
        time = datetime.now()
        secretkey = secrets.token_hex(8)
        bill = Bill(Time=time, Recipient="expense", Amount=1, Money=money, secret_key=secretkey,
                    User_Id=None, Airline_order=airline_order, State=False)
        bill.save()
        return JsonResponse({"payment_provider": "WH", "secret_key": bill.secret_key})


def Payment_Order(request):
    if request.method == 'POST':
        REquest = json.loads(request.body)
        ticket = REquest.get("uid") and REquest.get("Airline_order") and len(REquest) == 2
        if ticket:
            user_Id = REquest["uid"]
            airline_order = REquest["Airline_order"]
        bill = Bill.objects.get(Airline_order=airline_order)
        USER = User.objects.get(id=user_Id)
        if USER.deposit >= bill.money:
            bill.User_Id = USER
            bill.save()
            USER.save()
            return JsonResponse({"msg": bill.secret_key})
        else:
            return JsonResponse({"msg": "Money not enough. Please recharge the account."})


def Payment_Check(request):
    if request.method == 'POST':
        REquest = json.loads(request.body)
        ticket_state = REquest.get("state") and REquest.get("order_id") and len(REquest) == 2
        if ticket_state:
            payment_state = REquest["state"]
            airline_order = REquest["order_id"]
        if payment_state == "successful":
            payment_bill = Bill.objects.get(Airline_order=airline_order)
            payment_bill.State = True
            payment_bill.save()
            customer = User.objects.get(id=payment_bill.user_Id.id)
            customer.deposit = customer.deposit - payment_bill.money
            customer.save()
            return JsonResponse({"state": "paid"})
        else:
            return JsonResponse({"state": "unpaid"})


def Payment_Return(request):
    if request.method == 'POST':
        REquest = json.loads(request.body)
        ticket = REquest.get("state") and REquest.get("order_id") and len(REquest) == 2
        if ticket:
            state = REquest["state"]
            airline_order = REquest["order_id"]
        if state == "successful":
            cancel_bill = Bill.objects.get(airline_order=airline_order)
            cancel_bill.save()
            time = datetime.now()
            secretkey = secrets.token_hex(8)
            customer = User.objects.get(id=cancel_bill.user_Id.id)
            customer.deposit = float(customer.deposit) + float(customer.money)
            customer.save()
            return_bill = Bill(Time=time, Recipient="income", Amount=1, Money=cancel_bill.Money,
                               secret_key=secretkey, User_Id=customer, Airline_order=airline_order, state=True)
            return_bill.save()
            return JsonResponse({"state": "canceled"})
        else:
            return JsonResponse({"state": "uncanceled"})

def Transfer(request):
    if request.method == "POST":
        user = json.loads(request.body)
        user_id = user["uid"]
        password = user["password"]
        targetuser_name = user["u2"]
        check_username = user["u3"]
        money = user["money"]
        source_user = User.objects.filter(id=user_id).first()
        if password != source_user.password:
            return JsonResponse({"msg": "Invalid password."})
        if targetuser_name != check_username:
            return JsonResponse({"msg": "The usernames typed in are different. Please"
                                        "check"})
        target_user = User.objects.filter(username=targetuser_name).first()
        if target_user is None:
            return JsonResponse({"msg": "Invalid username for transference. Please"
                                        "check"})
        if source_user.deposit < money:
            return JsonResponse({"msg": "Deposit not enough."})
        source_user.deposit -= money
        target_user.deposit += money
        source_user.save()
        target_user.save()
        time = datetime.now()
        secretkey = secrets.token_hex(8)
        bill1 = Bill(Time=time, Recipient="expense", Amount=1, Money=money, secret_key=secretkey,
                       User_Id=source_user, Airline_order=0, State=True)
        bill2 = Bill(Time=time, Recipient="income", Amount=1, Money=money, secret_key=secretkey,
                       User_Id=target_user, Airline_order=0, State=True)
        bill1.save()
        bill2.save()
        return JsonResponse({"msg": "Successful transference."})


def Balance(request):
    if request.method == "POST":
        income = 0
        expense = 0
        balance_user = json.loads(request.body)
        balance_userid = balance_user["uid"]
        search_user = User.objects.filter(id=balance_userid).first()
        bill_records = Bill.objects.filter(userId=search_user, State=True).all()
        for x in bill_records:
            if x.recipient == "income":
                income += x.money
            else:
                expense += x.money
        balance = {"income": income, "expense": expense}
        return JsonResponse(balance, safe=False)

def Statement(request):
    if request.method == 'POST':
        REquest = json.loads(request.body)
        statement = REquest.get("uid") and len(REquest) == 1
        if statement:
            uid = REquest["uid"]
        query_bill = Bill.objects.all()
        target_user = User.objects.filter(id=uid).first()
        bill_list = {}
        n = 0
        for x in query_bill:
            if x.userId == target_user:
                add_bill = {"Time": x.time, "Money": x.money, "Recipient": x.recipient}
                bill_list[n] = add_bill
                n += 1
        return JsonResponse({"msg": bill_list})



