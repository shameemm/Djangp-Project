from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from users.models import *
import os
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django import template
import pandas as pd
from django.http import FileResponse
from guest_user.decorators import allow_guest_user



# Create your views here.
def adminlogin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminhome')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate( username=username, password=password)
        if user is not None and user.is_superuser==True:
            auth.login(request, user)
            return redirect('adminhome')
        else:
            print(password)
            messages.info(request, 'Invalid Cedentials')
            return redirect('adminlogin')
    else:
        return render(request, 'admins/admin_login.html')
    
def addcategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = Category.objects.create(name=name,description=description)
        category.save()
        return redirect('categories')
    else:
        return render(request, 'admins/add_category.html')
    
@login_required(login_url='adminlogin')
def category_block(request):
    id=request.GET['id']
    category=Category.objects.get(id=id)
    category.is_active=False
    print(category)
    category.save()
    return redirect('categories')

@login_required(login_url='adminlogin')
def category_unblock(request):
    id=request.GET['id']
    category=Category.objects.get(id=id)
    category.is_active=True
    print(category)
    category.save()
    return redirect('categories')

@login_required(login_url='adminlogin')
def delete_category(request):
    id=request.GET['id']
    category=Category.objects.filter(id=id)
    category.delete()
    return redirect('categories')

@login_required(login_url='adminlogin')    
def adminhome(request):
    orders=Order.objects.all()
    products=Product.objects.all()
    return render(request, 'admins/admin_home.html',{'orders':orders,'products':products})


@login_required(login_url='adminlogin')
def users(request):
    users = User.objects.filter(is_superuser=False, first_name__isnull=False)
    return render(request, 'admins/user_management.html', {'users':users})
@login_required(login_url='adminlogin')
def acceptrequest(request):
    id=request.GET['id']
    Order.objects.filter(id=id).update(status='Return Accepted')
    return redirect('order')

@login_required(login_url='adminlogin')
def rejectrequest(request):
    id=request.GET['id']
    Order.objects.filter(id=id).update(status='Return Rejected')
    return redirect('order')

@login_required(login_url='adminlogin')
def addproduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        brand = request.POST['brand']
        quantity = request.POST['quantity']
        print(request.FILES,"  1111")
        image = request.FILES['image']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        print(image1,"  2222")
        category=Category.objects.get(id=category)
        # image = Images.objects.create(image=image,product=product)
        product = Product.objects.create(name=name,description=description,price=price,category=category,image=image,brand=brand,quantity=quantity)
        product.save()
        
        image1 = Images.objects.create(image=image1,product=product)
        image1.save()
        image2 = Images.objects.create(image=image2,product=product)
        image2.save()
        image3 = Images.objects.create(image=image3,product=product)
        image3.save()
        return redirect('products')
    else:
        
        category=Category.objects.all()
        return render(request, 'admins/add_product.html',{'categories':category})
    
def cancelorder(request):
    user=request.user
    id=request.GET['id']
    Order.objects.filter(id=id).update(status='Cancelled',cancel=True)
    return redirect('order')


@login_required(login_url='adminlogin')
def products(request):
    product=Product.objects.all()
    return render(request, 'admins/product_management.html',{'products':product})

@login_required(login_url='adminlogin')
def sales(request):
    orders=Order.objects.all().order_by('-id')
    return render(request, 'admins/sales.html',{'orders':orders})

@login_required(login_url='adminlogin')
def order(request):
    order = Order.objects.all().order_by('-id')
    cart = Cart.objects.all()
    status = ['Shipped','Out of Delivery','Delivered']
    status1 = ['Out of Delivery','Delivered']
    status2 = ['Delivered']
    
    return render(request, 'admins/ordermanagement.html',{'orders':order,'carts':cart,'status':status,'status1':status1,'status2':status2})

@login_required(login_url='adminlogin')
def delete_product(request):
    id=request.GET['id']
    product=Product.objects.filter(id=id)
    product.delete()
    return redirect('products')

@login_required(login_url='adminlogin')
def edit_product(request):
    id=request.GET['id']
    prod = Product.objects.get(id=id)
    if request.method=='POST':
        id=request.GET['id']
        prod = Product.objects.get(id=id)
        print(id)
        
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        brand = request.POST['brand']
        print(request.FILES,"  1111")
        image = request.FILES['image']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        quantity = request.POST['quantity']
        
        category=Category.objects.get(id=category)
        product = Product.objects.get(id=id)
        product.name=name
        product.description=description
        product.price=price
        product.category=category
        product.brand=brand
        product.quantity=quantity
        product.image=image
        product.save()
        
        return redirect('products')
    else:
        id=request.GET['id']
        product=Product.objects.get(id=id)
        category=Category.objects.all()
        return render(request, 'admins/edit_product.html',{'product':product,'categories':category})
@login_required(login_url='adminlogin')
def block(request):
    id=request.GET['id']
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('users')
@login_required(login_url='adminlogin')
def offers(request):
    offer=Offers.objects.all().order_by('-id')
    return render(request, 'admins/offer_management.html',{'offers':offer}) 

@login_required(login_url='adminlogin')
def addoffer(request):
    if request.method == 'POST':
        name = request.POST['name']
        offer = request.POST['offer']
        startdate = request.POST['startdate']
        max_value = request.POST['max_value']
        print(startdate)
        enddate = request.POST['enddate']
        print( "end",enddate)
        category = request.POST['category']
        product = request.POST['product']
        print(product)
        offer = Offers.objects.create(name=name,offer=offer,start_date=startdate,end_date=enddate,category_id=category,product_id=product,max_value=max_value)
        offer.save()
        return redirect('offers')
    else:
        products=Product.objects.all()
        categories=Category.objects.all()
        return render(request, "admins/add_offer.html",{'products':products,'categories':categories})
    
@login_required(login_url='adminlogin')
def report(request):
    print(request.method)
    start = request.POST['start_date']
    end = request.POST['end_date']
    print("end=",end)
    order = Order.objects.filter(ordered_date__range=[start,end])
    print(order)
    type = request.POST['type']
    # order = Order.objects.all()
    print(type)
    if type == 'PDF':
        
        template_path = 'admins/report.html'

        context = {'order': order}

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="invoice.pdf"'

        template = get_template(template_path)

        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        data =[]
        for order in order:
            data.append({
                "id":order.id,
                "Customer":order.user.username,
                "Ordered date":str(order.ordered_date),
                "Amount":order.amount,
                "Payment Method":order.method,
                "Order Status":order.status,
            })
        pd.DataFrame(data).to_excel("report.xlsx")
        # response['Content-Disposition'] = 'filename="report.xlsx"'
        return FileResponse(open('report.xlsx', 'rb'), as_attachment=True, filename="report.xlsx")
        
@login_required(login_url='adminlogin')
def yearly(request):
    year = request.POST['year']
    type = request.POST['type']
    order = Order.objects.filter(ordered_date__year=year)
    if type == 'PDF':
        
        template_path = 'admins/report.html'

        context = {'order': order}

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="invoice.pdf"'

        template = get_template(template_path)

        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        data =[]
        for order in order:
            data.append({
                "id":order.id,
                "Customer":order.user.username,
                "Ordered date":str(order.ordered_date),
                "Amount":order.amount,
                "Payment Method":order.method,
                "Order Status":order.status,
            })
        pd.DataFrame(data).to_excel("report.xlsx")
        # response['Content-Disposition'] = 'filename="report.xlsx"'
        return FileResponse(open('report.xlsx', 'rb'), as_attachment=True, filename="report.xlsx")
@login_required(login_url='adminlogin')
def monthly(request):
    month = request.POST['month']
    type = request.POST['type']
    order = Order.objects.filter(ordered_date__month=month)
    if type == 'PDF':
        
        template_path = 'admins/report.html'

        context = {'order': order}

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="invoice.pdf"'

        template = get_template(template_path)

        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        data =[]
        for order in order:
            data.append({
                "id":order.id,
                "Customer":order.user.username,
                "Ordered date":str(order.ordered_date),
                "Amount":order.amount,
                "Payment Method":order.method,
                "Order Status":order.status,
            })
        pd.DataFrame(data).to_excel("report.xlsx")
        # response['Content-Disposition'] = 'filename="report.xlsx"'
        return FileResponse(open('report.xlsx', 'rb'), as_attachment=True, filename="report.xlsx")

@login_required(login_url='adminlogin')
def blockcoupon(request):
    id=request.GET['id']
    offer=Offers.objects.filter(id=id).update(is_active=False)
    
    return redirect('offers')

@login_required(login_url='adminlogin')
def unblockcoupon(request):
    id=request.GET['id']
    offer=Offers.objects.filter(id=id).update(is_active=True)
    
    return redirect('offers')

@login_required(login_url='adminlogin')
def updatestatus(request):
    id=request.GET['id']
    status=request.POST['status']
    
    print(id,status)
    Order.objects.filter(id=id).update(status=status)
    return redirect('order')

@login_required(login_url='adminlogin')
def coupons(request):
    coupon=Coupon.objects.all()
    return render(request, 'admins/coupon_management.html',{'coupons':coupon})

def addcoupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        start_date = request.POST['startdate']
        end_date = request.POST['enddate']
        coupon = Coupon.objects.create(code=code,discount=discount,start_date=start_date,end_date=end_date)
        return redirect('coupons')
    else:
        return render(request, "admins/add_coupon.html")
@login_required(login_url='adminlogin')
def unblock(request):
    id=request.GET['id']
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('users')
@login_required(login_url='adminlogin')
def categories(request):
    category=Category.objects.all()
    return render(request, 'admins/category_management.html',{'categories':category})
@login_required(login_url='adminlogin')
def adminlogout(request):
    auth.logout(request)
    return redirect('adminlogin')