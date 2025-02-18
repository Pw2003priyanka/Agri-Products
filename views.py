from typing import Any
from django.shortcuts import render,redirect, get_object_or_404
from .models import product,customer,agriagency,cart,order,payment,orderdetail
from django.http import HttpResponse
from django.views.generic import DeleteView,ListView,CreateView,UpdateView,DetailView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from django.template import loader
from datetime import date
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.shortcuts import render

# Create your views here.
class productview(ListView):
    model=product
    template_name='productview.html'
    context_object_name='probj'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

    def product_view(request):
        if request.method=="GET":
            return render(request,'productview.html')
        
def search(request):
    if request.method=="POST":
        searchdata=request.POST.get('searchquery')
        probj=product.objects.filter(Q(product_name__icontains=searchdata) | Q(product_price__icontains=searchdata))
        return render(request,'productview.html',{'probj':probj})
    
class productdetail(DetailView):
    model=product
    template_name="productdetail.html"
    context_object_name="d"


class agriagencyview(ListView):
    model=agriagency
    template_name='index.html'
    context_object_name='agriobj'

    def agriagencyview(request):
        if request.method == "GET" :
            return render(request, 'index.html')
    

def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    elif request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        password=request.POST.get('password')
        epassword=make_password(password)

        cusobj=customer(name=name,email=email,phoneno=phoneno,password=epassword)
        cusobj.save()
        return redirect('../login/')
    
    
def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method =="POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        cust = customer.objects.filter(email=email)
        if cust:
            custobj = customer.objects.get(email=email)

            flag = check_password(password,custobj.password)

            if True:
                request.session['sessionvalue']=  custobj.email
                agriobj=agriagency.objects.all()
                print(agriobj)
                return render(request,'index.html',{"agriobj":agriobj})
            else:
                return render(request,'login.html',{'msg':'Incorrect username and Password'})
            
        else:
            return render(request,'login.html',{'msg':'Incorrect username and Password'})
        

def agriregister(request):
    if request.method=="GET":
        return render(request,'agriregister.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        # Continue with the rest of your code
        image=request.FILES.get('image')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        password=request.POST.get('password')
        description=request.POST.get('description')
        epassword=make_password(password)

        agrilogobj=agriagency(image=image,name=name,email=email,phoneno=phoneno,password=epassword,description=description)
        agrilogobj.save()
        return redirect('../agrilogin/')
    
def agrilogin(request):
    if request.method=="GET":
        return render(request,'agrilogin.html')
    if request.method =="POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        agrilog = agriagency.objects.filter(email=email)
        if agrilog:
            agrilogobj = agriagency.objects.get(email=email)
            print(agrilogobj)
            flag = check_password(password,agrilogobj.password)
            print(flag)

    
            if True:
                request.session['sessionvalueagriagency']=  agrilogobj.email
                return redirect('../profile/')
            else:
                return render(request,'agrilogin.html',{'msg':'Incorrect username and Password'})
            
        else:
            return render(request,'agrilogin.html',{'msg':'Incorrect username and Password'})
        


def agriagencynavbar(request):
    return render(request,'agrinavbar.html')

def agriagencyprofile(request):
    agriagencysess = request.session['sessionvalueagriagency']
    agrilog = agriagency.objects.filter(email=agriagencysess)

    agrilogobj = None  # Initialize the variable with a default value
    if agrilog:
        agrilogobj = agriagency.objects.get(email=agriagencysess)

    return render(request, 'profile.html', {'session': agriagencysess, 'agrilogobj': agrilogobj})

def agrieditprofile(request):
    if request.method == 'GET':
        return render(request,'agrieditprofile.html')
    if request.method == 'POST':
        image=request.FILES.get('image')
        name = request.POST.get('name')
        # image=request.FILES.get('image')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        description=request.POST.get('description')
            
        agriagencysess=request.session['sessionvalueagriagency']
        agrilog=agriagency.objects.filter(email=agriagencysess).update(image=image,name=name,email=email,phoneno=phoneno,description=description)
        return redirect('../profile/')
    
def addproduct(request):

    if request.method == 'POST':
       
        iid=request.POST.get('iid')
        agriagencysess=request.session['sessionvalueagriagency']
        agrilogobj=agriagency.objects.get(email=agriagencysess)

        image=request.FILES.get('image')
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        # name=request.POST.get('name')
        product_price= request.POST.get('product_price')
       
        
        new_product = product(
            image=image,
            product_name=product_name,
            product_description=product_description,
            # name=name,
            product_price=product_price,
            agriagencyid=agrilogobj
        )
        new_product.save()

        return redirect('../viewproduct/')  



    return render(request, 'addproduct.html')



def viewproduct(request):
    agriagencysess=request.session['sessionvalueagriagency']
    
    agrilog=agriagency.objects.filter(email=agriagencysess)
    if agrilog:

        agrilogobj=agriagency.objects.get(email=agriagencysess)
        cobj=product.objects.filter(agriagencyid=agrilogobj.id)
       

        return render(request,'viewproduct.html',{'cobj':cobj})

 
class deleteproduct(DeleteView):
    model = product
    template_name='deletetask.html'
    success_url=reverse_lazy('viewproduct')

class detailproduct(DetailView):
    model =product
    template_name = 'productdetail.html'
    context_object_name='i'


def editproduct(request, pk):
    product_obj = get_object_or_404(product, id=pk)

    if request.method == 'POST':
        product_obj.product_name = request.POST.get('product_name')
        product_obj.product_description = request.POST.get('description')
        product_obj.product_price = request.POST.get('product_price')
        

        
        if 'image' in request.FILES:
            product_obj.image = request.FILES['image']

        
        product_obj.save()

        return redirect('../viewproduct/', product_id=product_obj.id)
    
    context = {
        'product': product,
        'cobj': product_obj
    }


    return render(request, 'editproduct.html', context)


def agriagencylogout(request):
    del(request.session['sessionvalueagriagency'])
    return redirect('../agrilogin')   

def addtocart(request):
    productid = request.POST.get('productid')
    print(productid)
    cussession = request.session['sessionvalue'] #email of customer
    cusobj = customer.objects.get(email = cussession) #fetch record from database table using email
    #fetch customer id using customer object
    probj = product.objects.get(id=productid)

    flag = cart.objects.filter(custid = cusobj.id,pac = probj.id)
    if flag:
        cartobj = cart.objects.get(custid = cusobj.id,pac = probj.id)
        cartobj.quantity = cartobj.quantity +1
        cartobj.totalamount = probj.product_price * cartobj.quantity
        cartobj.save()
    else:
        cartobj = cart(custid = cusobj,pac = probj,quantity = 1,totalamount = probj.product_price*1)
        cartobj.save()

    return redirect('../productview/')


def viewcart(request):
    cussession = request.session['sessionvalue'] #email of customer
    cusobj = customer.objects.get(email = cussession) 
    cartobj = cart.objects.filter(custid = cusobj.id)

    return render(request,'viewcart.html',{'cartobj':cartobj,'session':cussession })

def cq(request):
    cemail =request.session['sessionvalue']
    pac=request.POST.get('pac')
    custobj=customer.objects.get(email=cemail)
    pacbj=product.objects.get(id=pac)
    cartobj=cart.objects.get(custid=custobj.id,pac=pacbj.id)

    if request.POST.get('changequantitybutton')=='+':
        cartobj.quantity=cartobj.quantity+1
        cartobj.totalamount=cartobj.quantity*pacbj.product_price
        cartobj.save()

    elif request.POST.get('changequantitybutton')=='-':
        print("inside- quantity")
        if cartobj.quantity==1:
            cartobj.delete()
        else:
            cartobj.quantity=cartobj.quantity-1
            cartobj.totalamount=cartobj.quantity*pacbj.product_price
            cartobj.save()

    return redirect('../viewcart/')

def summary(request):
    cussession=request.session['sessionvalue']
    cusobj=customer.objects.get(email=cussession)
    cartobj=cart.objects.filter(custid=cusobj.id)
    totalbill=0
    for i in cartobj:
        totalbill=i.totalamount+totalbill
    return render(request,'summary.html',{'session':cussession,'cartobj':cartobj,'totalbill':totalbill})

def placeorder(request):
    name=request.POST.get('name')
    phoneno=request.POST.get('phoneno')
    address=request.POST.get('address')
    city=request.POST.get('city')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
   

    datev=date.today()
    print(datev)
    orderobj=order(name=name,phoneno=phoneno,address=address,city=city,state=state,pincode=pincode,orderstatus='pending',orderdate=datev)
    orderobj.save()
    

    ono=str(orderobj.id)+str(datev).replace('-','')
    orderobj.ordernumber=ono
    orderobj.save()

    cussession=request.session['sessionvalue']
    cusobj=customer.objects.get(email=cussession)
    cartobj=cart.objects.filter(custid=cusobj.id)

    totalbill = 0 
    for i in cartobj:
        totalbill=i.totalamount+totalbill

    
    return render(request,'payment.html',{'orderobj':orderobj,'session':cussession,'cartobj':cartobj,'totalbill':totalbill})

def order_detail(request):
    cussession = request.session['sessionvalue']
    cusobj = customer.objects.get(email=cussession)
    orders = order.objects.filter(firstname=cusobj.name)

    return render(request, 'orderdetail.html', {'session': cussession, 'orders': orders})


def success(request):
    orderid = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    request.session['sessionvalue'] = request.GET.get('session')
    cussession=request.session['sessionvalue']
    cusobj=customer.objects.get(email=cussession)
    cartobj=cart.objects.filter(custid=cusobj.id)
    orderobj=order.objects.get(ordernumber = orderid)

    paymentobj=payment(customerid=cusobj,oid=orderobj,paymentstatus="Paid",transactionid=tid)
    paymentobj.save()

    for i in cartobj:
        orderdetailobj=orderdetail(paymentid=paymentobj,ordernumber=orderid,productid=i.pac,customerid=i.custid,quantity=i.quantity,totalprice=i.totalamount)
        orderdetailobj.save()
        i.delete()

    totalbill = 0
    for i in cartobj:
        totalbill = i.totalamount + totalbill

    return render(request,'success.html',{'session':cussession,'payobj':paymentobj, 'order':orderobj, 'cartobj': cartobj,  'totalbill' :totalbill})



def my_order(request):
    cussession = request.session['sessionvalue']
    cusobj = customer.objects.get(email=cussession)
    my_order = orderdetail.objects.filter(customerid=cusobj.id)

    return render(request, 'my_order.html', {'session': cussession, 'my_order': my_order})

def logout(request):
    del(request.session['sessionvalue'])
    return redirect('../index/')

def About(request):
    return render(request,'Agriapp/about.html')








# Create your views here.
