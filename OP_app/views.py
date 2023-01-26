from email import message
import re
from django.shortcuts import redirect, render
from .models import Contact,User
import random
from django.core.mail import send_mail
from OP_project import settings
from OP_app.models import *
import datetime
# Create your views here.



def index(request):
                     
    category = Product_category.objects.all()
    products = Product.objects.all()
   
    # print("category : ",category)
    context = {'category':category,'products':products}
    return render(request,"index.html",context) 

def contact(request):
    if request.method == "POST":
        print("-------------called POST block-----------")
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']

        print("------",fullname)
        print("------",email)
        print("------",message)

        Contact.objects.create(name=fullname,email=email,message=message)
        
        msg = "Your message saved succesfully."
        context = {'msg':msg}
        return render(request,"contact.html",context)
    
    else:
        print("-------------called else block-----------")
        return render(request,"contact.html")


def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mno = request.POST['mno']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        print(fname,lname,email,mno,password,cpassword)
        try:
            user_obj = User.objects.get(email=email)
            if user_obj:
                msg = "you are already register, please do login."
                messages = {'msg':msg}
                return render(request,"login.html",messages)    
        except:
            if password==cpassword:
                User.objects.create(firstname=fname,
                                    lastname=lname,
                                    email=email,
                                    mobile_no=mno,
                                    password=password)
                
                #generate otp
                gen_otp = random.randint(1000,9999)
                print("---->",gen_otp)
                request.session['gen_otp'] = gen_otp

                subject = "OTP Verification - OM Polymers"
                msg = "Your OTP is "+str(gen_otp)+" for sign up Verifivation"
                from_email = settings.EMAIL_HOST_USER
                to_email = [email, ]

                #send mail to user
                send_mail(subject,msg,from_email,to_email)

                context = {'gen_otp':gen_otp,'email':email}

                return render(request,'otp.html',context)
            else:
                msg = "Incorrect password and confirm password !!"
                messages = {'msg':msg}
                return render(request,"signup.html",messages)    

    else:
        return render(request,'signup.html')

def otp_verification(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        gen_otp = request.POST['gen_otp']
        email = request.POST['email']

        print("session otp : ",gen_otp)
        if user_otp == gen_otp:
            user_obj = User.objects.get(email=email)
            user_obj.status = "Active"
            user_obj.save()
            request.session['email'] = user_obj.email
            request.session['user_name'] = user_obj.firstname + " " + user_obj.lastname
            return redirect('index')
        else:
            msg = "OTP In correct !"
            context = {'msg':msg,'gen_otp':gen_otp,'email':email}
            return render(request,'otp.html',context)
    else:
        return render(request,"otp.html")



def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            user_obj = User.objects.get(email=email)
            if user_obj:
                if user_obj.status =="Active":
                    if user_obj.password == password:
                        request.session['email'] = user_obj.email
                        request.session['user_name'] = user_obj.firstname + " " + user_obj.lastname
                        return redirect("index")
                    else:
                        msg = "your password is incorrect."
                        context = {'msg':msg}
                        return render(request,"login.html",context)

                else:
                        msg = "you are not active user."
                        context = {'msg':msg}
                        return render(request,"login.html",context)   

        except:
            msg = "This email is not registered with us"
            context = {'msg':msg}
            return render(request,"login.html",context)        
                
    else:
        return render(request,'login.html')

def logout(request):
    del request.session['user_name']
    del request.session['email']
    return redirect('index') 
    # return render(request,'index.html')

def shop(request):
    products = Product.objects.all()
    category = Product_category.objects.all()
    print(products)
    context = {'products':products,'category':category}
    return render(request,'shop.html',context)

def cat_filter(request,pk):
    cat = Product_category.objects.get(pk=pk)
    products = Product.objects.filter(product_category=cat)
    context = {'products':products,'single_cat':cat}

    return render(request,'shop1.html',context)

def single_product(request,pk):
    Prod_obj = Product.objects.get(pk=pk)
    print("------------------>",Prod_obj)
    context = {'product':Prod_obj}

    return render(request,'single_product.html',context)


def about(request):
    return render(request,'about.html')    

def cart(request):
    try:
        # print("email-->",request.session['email'])
        user = User.objects.get(email=request.session['email'])
        cart_product = Cart.objects.filter(user=user)
        # print("Cart product-->",cart_product)
        sub_total = 0
        dilvery_charge = 0
        for pro in cart_product:
            sub_total = sub_total + pro.total_price
        final_total = sub_total + dilvery_charge

        context = {'cart_product':cart_product,'sub_total':sub_total,'final_total':final_total,'dilvery_charge':dilvery_charge}
        return render(request,'cart.html',context)
       
    except Exception as e:
        print("---->",e)
        msg = "Please First do login !"
        context = {'msg':msg}
        return render(request,'login.html',context)


def add_to_cart(request,pk):
    try:
        # import pdb;pdb.set_trace()
        product = Product.objects.get(pk=pk)
        user = User.objects.get(email=request.session['email'])
        cart_product = Cart.objects.filter(user=user)
      

        pro_qty =request.POST['pro_qty']
        print(type(pro_qty))

        total_price = product.Product_price * int(pro_qty)

        try:
            cart_obj = Cart.objects.get(product_id=product,user=user)
            
            cart_obj.product_qty = cart_obj.product_qty+int(pro_qty)
            cart_obj.save()
            cart_obj.total_price = product.Product_price *  int(cart_obj.product_qty)
            cart_obj.save()
            print("qty -->",cart_obj)
        except Exception as e:
            print("---->",e)
            Cart.objects.create(user=user,
                                product_id=product,
                                product_qty=pro_qty,
                                total_price=total_price,
                                dateTime=datetime.datetime.now())

            
        context = {'cart_product':cart_product}
        # return render(request,'cart.html',context)
        return redirect('cart')
    except Exception as e:
        print("---->",e)
        msg = "Please First do login !"
        context = {'msg':msg}
        return render(request,'login.html',context)

def wishlist(request):
    try:
        user = User.objects.get(email=request.session['email'])
        wishlist_product = Wishlist.objects.filter(user=user)
        context = {'wishlist_product':wishlist_product}
        return render(request,'Wishlist.html',context)
       
    except Exception as e:
        print("---->",e)
        msg = "Please First do login !"
        context = {'msg':msg}
        return render(request,'login.html',context)
        
def remove_product(request,pk):
    Cart.objects.filter(pk=pk).delete()
    return redirect('cart')

def remove_wishlist(request,pk):
    Wishlist.objects.filter(pk=pk).delete()
    return redirect('wishlist')    

def invoice(request):
    return render(request,"invoice.html")

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
 


def checkout(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=int(amount),
                                                       currency='INR',
                                                       payment_capture='1'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    
   
 




    email = request.session['email']
    user = User.objects.get(email=email)
    cart_product = Cart.objects.filter(user=user)

    print("--------cart product--------")
    print(cart_product)
    sub_total = 0
    dilivery_charge = 0

    for product in cart_product:
        sub_total = sub_total + product.total_price
    
    sub_total = sub_total + dilivery_charge
    final_total = sub_total

    context = {'sub_total':sub_total,"final_total":final_total, "cart_product":cart_product}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_API_KEY
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url  
    return render(request,"checkout.html",context)


 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'invoice.html')
                except:
 
                    # if there is an error while capturing payment.
                    return redirect("checkout")
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()