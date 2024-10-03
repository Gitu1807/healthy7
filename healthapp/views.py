from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages  # Import messages module
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import razorpay , random , re 
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import product, Cart, Order


# Create your views here.
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm


#for mail (contact us)
from django.conf import settings
from django.http import JsonResponse


def home(request):
    return render(request,'index.html')

def products(request):
    p=product.objects.filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'meds.html',context)

def search(request):
    query=request.GET['query']
    cname=product.objects.filter(name__icontains=query)
    cat=product.objects.filter(cat__icontains=query)
    cdetail=product.objects.filter(cdetail__icontains=query)
    allprod=cname.union(cat,cdetail)
    context={}
    if allprod.count()==0:
        context['errmsg']='Course Not Found'
    context['data']=allprod
    return render(request,'meds.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'meds.html',context)

def sortbyprice(request,sv):
    if sv=='1':
        p=product.objects.order_by('price')
    else:
        p=product.objects.order_by('-price')

    context={}
    context['data']=p
    return render(request,'meds.html',context)

def medsdetail(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'meds_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        #uid=request.user.id
        context={}
        u=User.objects.filter(id=request.user.id)
        p=product.objects.filter(id=pid)
        # check product is exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context['data']=p
        if n==1:
            context['errmsg']="Product Already exist"
            return render(request,'meds_details.html',context)
        else:
            c=Cart.objects.create(uid = u[0],pid = p[0])
            c.save()
            context['msg']="Product added Successfully in the cart"
            return render(request,'meds_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    context={}
    context['data']=c
    sum=0
    for x in c:
        sum=sum+x.pid.price*x.qty
    context['total']=sum
    context['n']=len(c)
    return render(request,'myorders.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty

    if x == '1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/viewcart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/orders')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amt=x.qty*x.pid.price
        o=Order.objects.create(orderid=orderid,pid=x.pid,uid=x.uid,qty=x.qty,amount=amt)
        o.save()
        x.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={'data':o}
    sum=0
    for x in o:
        sum=sum+x.amount
    context['total']=sum
    context['n']=len(o)
    return render(request,'placeorder.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_a8l74eTlnJiAdH", "e0MI8JumWDHYgha4OOoKZFkV"))
    o=Order.objects.filter(uid=request.user.id)
    sum=0
    for x in o:
        sum=sum+x.amount
        oid=x.orderid
    data = { "amount": sum*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['payment']=payment
    return render(request,'pay.html',context)

def paymentsuccess(request):
    sub='Payment Confirmation - Thank You for Your Purchase!'
    msg='Dear User,We are thrilled to confirm that your payment for the product on Healthy SEVEN has been successfully processed. Thank you for choosing us as your partner in Health!'
    frm='rxjpatil@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )

    Order.objects.filter(uid=request.user.id).delete()
    return render(request,'paymentsuccess.html')
# Product Section ends

def bmi(request):
    return render(request,'bmi.html')

def mental(request):
    return render(request,'mental.html')

def dietnut(request):
    return render(request,'dietnut.html')

def sleep(request):
    return render(request,'sleep.html')

def vision(request):
    return render(request,'vision.html')

# For Level-Up section

def diet(request):
    return render(request,'diet.html')

def obasity(request):
    return render(request,'obasity.html')

def underweight(request):
    return render(request,'underweight.html')

def mentalhealth(request):
    return render(request,'mentalhealth.html')

def goals(request):
    return render(request,'goals.html')

# Blog Section

def blogs(request):
    return render(request,'blogs.html')

def news(request):
    return render(request,'news.html')

def daily(request):
    return render(request,'daily.html')

def appointment(request):
    return render(request,'appointment.html')



def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        context = {}
        n = request.POST['uname']
        p = request.POST['upass']
        cp = request.POST['ucpass']

        # Updated regex to correctly match email formats with allowed domains (gmail, yahoo, outlook)
        email_regex = r'^[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook)\.com$'

        has_alphabet = any(c.isalpha() for c in n)
        has_number = any(c.isdigit() for c in n)

        if n == '' or p == '' or cp == '':
            context['errmsg'] = 'Field cannot be blank'
            return render(request, 'register.html', context)
        elif not re.match(email_regex, n):
            context['errmsg'] = 'Invalid email format. Only gmail, yahoo, or outlook domains are allowed.'
            return render(request, 'register.html', context)
        elif not has_alphabet or not has_number:
            context['errmsg'] = 'Email must contain at least one alphabet and one number.'
            return render(request, 'register.html', context)
        elif len(p) < 8:
            context['errmsg'] = 'Password must be at least 8 characters long.'
            return render(request, 'register.html', context)
        elif p != cp:
            context['errmsg'] = 'Password and Confirm Password must match.'
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(username=n, email=n)
                u.set_password(p)
                u.save()
                context['success'] = 'User Created Successfully'
                return render(request, 'register.html', context)
            except Exception as e:
                context['errmsg'] = "User already exists, please login!"
                return render(request, 'register.html', context)


# def register(request):
#     if request.method=='GET':
#         return render(request,'register.html')
#     else:
#         context={}
#         n=request.POST['uname']
#         p=request.POST['upass']
#         cp=request.POST['ucpass']

#         if n=='' or p=='' or cp=='':
#             context['errmsg']='Field can not be blank'
#             return render(request,'register.html',context)
#         elif len(p)<=8:
#             context['errmsg']='password must be atleast 8 character'
#             return render(request,'register.html',context)
#         elif p!=cp:
#             context['errmsg']='password and confirm password must be same'
#             return render(request,'register.html',context)
#         else:
#             try:
#                 u=User.objects.create(username=n,email=n)
#                 u.set_password(p )
#                 u.save()
#                 context['success']='User Created Successfully'
#                 return render(request,'register.html',context)
#             except Exception:
#                 context['errmsg']="User already Exist, Please Login!"
#                 return render(request,'register.html',context)

def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']

        u=authenticate(username=n,password=p)
        if u is not None:
            login(request,u)
            return redirect('/home')
        else:
            context={}
            context['errmsg']='Invalid Username and Password'
            return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/home')

# ********************************PASSWORD***************************************


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})

def dashboard(request):
    u=User.objects.filter(id=request.user.id)
    context={}
    context['data1']=u
    return render(request,'profile.html',context)

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Validate form fields
        if not name or not email or not subject or not message:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        # Send email
        try:
            send_mail(
                subject,
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_US_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'success': 'Message sent successfully!'})
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while sending the message'}, status=500)