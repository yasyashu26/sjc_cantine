from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from staff_admin.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from inventory.models import Order, Product, Cart, total_order
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

@login_required
@staff_member_required
def admin_home(request):
    return render(request,'admin_home.html')

@login_required
@staff_member_required
def inventory_mgmt(request):
    items = Product.objects.all()
    context = {'items':items}
    return render(request, 'inventory.html', context)

@login_required
@staff_member_required
def add_items(request):
    form = ProductForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request,"Item Added Successfully.")
        return redirect('add_items')
    form = ProductForm()
    context = {'form': form}
    return render(request, 'add_items.html', context)

@login_required
@staff_member_required
def edit_item(request, pk): 
    instance = get_object_or_404(Product, pk=pk)
    form = ProductForm( data=(request.POST or None),files=(request.FILES or None),instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request,"Item Edited Successfully.")
        return redirect('inventory_mgmt')
    return render(request, 'add_items.html', {'form': form}) 

@login_required
@staff_member_required
def delete_items(request,pk):
    item = get_object_or_404(Product, pk=pk)
    item.delete()
    messages.error(request,"Item Deleted Successfully.")
    return redirect('inventory_mgmt')




#order paid button status executes
@login_required
@staff_member_required
def order_paid_btn(request, pk):
    item = get_object_or_404(Order, pk=pk)
    item.paid='yes'
    item.save()
    messages.success(request, "Order Payment Success")
    return redirect('awaited_orders')



#order paid button status executes
@login_required
@staff_member_required
def order_cancelled_btn(request, pk):
    item = get_object_or_404(Order, pk=pk)
    item.paid='no'
    item.save()
    messages.error(request, "Order Cancelled")
    return redirect('awaited_orders')

@login_required
@staff_member_required
def awaited_orders(request):
    queryset = Order.objects.filter(paid='null', ordered=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)

    try:
        aw_orders = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        aw_orders = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        aw_orders = paginator.page(paginator.num_pages)
    return render(request, 'awaited_orders.html',{'aw_orders':aw_orders})



@login_required
@staff_member_required
def all_paid_orders(request):
    queryset=Order.objects.filter(paid='yes', delivered='null')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        pd_orders = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        pd_orders = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        pd_orders = paginator.page(paginator.num_pages)
    return render(request, 'paid_orders.html',{'pd_orders':pd_orders})


#################################################################################################################
@login_required
@staff_member_required
def order_delivered_btn(request, pk):
    item = get_object_or_404(Order, pk=pk)
    item.delivered='yes' 
    item.save()
    current_order=Order.objects.filter(pk=pk)
    list_items = current_order.values_list('orderitems__id', flat=True)
    for item in list_items:
        item = get_object_or_404(Cart, pk=item)
        item.served=True
        item.served_date=timezone.now()
        item.save()
    messages.success(request, "Order Served")
    return redirect('all_paid_orders')




#search bar
@login_required
@staff_member_required
def search(request):        
    if request.method == 'POST':      
        orderid = request.POST.get('search')      
        if orderid:
            aw_orders = Order.objects.filter( pk=orderid,paid='null', ordered=True)   
            if aw_orders:
                return render(request,'awaited_orders.html',{'aw_orders':aw_orders})
            else:
                messages.warning(request, "No Order Found!")
                return redirect('awaited_orders')
        else:
            messages.warning(request, "Enter Valid Order ID")
            return redirect('awaited_orders')
    else:
        return redirect('awaited_orders')

@login_required
@staff_member_required
def search_po(request):        
    if request.method == 'POST':      
        orderid = request.POST.get('search')      
        if orderid:
            pd_orders = Order.objects.filter( pk=orderid, paid='yes', delivered='null')   
            if pd_orders:
                return render(request,'paid_orders.html',{'pd_orders':pd_orders})
            else:
                messages.warning(request, "No Paid Order Found!")
                return redirect('all_paid_orders')
        else:
            messages.warning(request, "Enter Valid Order ID")
            return redirect('all_paid_orders')
    else:
        return redirect('all_paid_orders')

@login_required
@staff_member_required
def available(request, pk):
    item = get_object_or_404(Product, pk=pk)
    item.available =True
    item.save()
    messages.success(request,"Item Marked Available")
    return redirect('inventory_mgmt')
    


@login_required
@staff_member_required
def not_available(request, pk):
    item = get_object_or_404(Product, pk=pk)
    item.available =False
    item.save()
    messages.error(request,"Item Marked Not Available")
    return redirect('inventory_mgmt')

    
@login_required
@staff_member_required
def show_total_orders(request):
    total_order.objects.all().delete()
    cart_items = Cart.objects.filter(served=True)
    for cart_item in cart_items:
        t_o, created =  total_order.objects.get_or_create( item = cart_item.item)
        t_o.total_items += cart_item.quantity 
        t_o.save()

    served_orders = total_order.objects.all()
    context = {'total_order':served_orders}
    return render(request, 'show_served_orders.html',context )

