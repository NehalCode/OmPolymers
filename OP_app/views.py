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
                request.session['user_name'] = fname + " " + lname
                

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
            request.session['user_name'] = user_obj.firstname + " " + user_obj.lastname
            return render(request,'index.html')
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
                        return render(request,"index.html")
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
            print(pro.__dict__)
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
        product = Product.objects.get(pk=pk)
        user = User.objects.get(email=request.session['email'])
        cart_product = Cart.objects.filter(user=user)
      

        pro_qty =request.POST['pro_qty']
        print(type(pro_qty))

        total_price = product.Product_price * int(pro_qty)

        try:
            cart_obj = Cart.objects.get(product_id=product,user=user)
            cart_obj.product_qty = cart_obj.product_qty+1
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