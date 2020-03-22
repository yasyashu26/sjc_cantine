from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import ListView
from inventory.models import Product,Order,Cart, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    categories = Category.objects.all()
    context={'categories':categories}
    return render(request, 'home.html',context)


def products(request, pk):
    products=Product.objects.filter(category=pk)
    category=Category.objects.get(pk=pk)
    category_name=category.title
    context ={'products':products,'category_name':category_name}
    return render(request, 'products.html', context)




@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        purchased=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            order.orderitems.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Remove item from cart
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__pk=item.pk).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, "This item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Cart View
@login_required
def CartView(request):

    user = request.user

    carts = Cart.objects.filter(user=user, purchased=False)
    orders = Order.objects.filter(user=user, ordered=False)

    if carts.exists():
        if orders.exists():
            order = orders[0]
            return render(request, 'cart.html', {"carts": carts, 'order': order})
        else:
            messages.warning(request, "You do not have any item in your Cart")
            return redirect("home")
		
    else:
        messages.warning(request, "You do not have any item in your Cart")
        return redirect("home")


@login_required
##decrease item count from count
def decreaseCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__pk=item.pk).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            ).last()
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} has been Updated.")
                return redirect("cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request, f"{item.name} has been removed from Cart.")
                return redirect("cart")
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("home")




@login_required
def checkout(request):
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    
    order_m_t = Order.objects.get(user=request.user, ordered=False)
    order_m_t.total_price = order_qs.last().get_totals()
    order_m_t.ordered = True
    order_m_t.save()
    cartItems = Cart.objects.filter(user=request.user, purchased=False)
    for item in cartItems:
        item.purchased = True
        item.save()
    messages.info(request,"your order %r confirmed"%(order_m_t.pk))
    return redirect('checkout_page')
    
@login_required
# Checkout view
def checkout_page(request):
    #order_qs = Order.objects.filter(user= request.user, ordered=True)
    orders = Order.objects.filter(user=request.user, ordered=True, delivered='null').order_by('pk').reverse()
    context = {"orders":orders}
    return render(request, 'checkout.html', context)

@login_required
def pastorders(request):
    orders_list = Order.objects.filter(user=request.user, ordered=True, delivered='yes')
    queryset =orders_list.order_by("pk").reverse()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        orders = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        orders = paginator.page(paginator.num_pages)

    context = {"orders":orders}
    return render(request, 'past_orders.html', context)


def about(request):
    return render(request,'about.html',{})


#def cart_sync(request, room_name):
 #   return render(request, 'cart.html', {
  #      'room_name': room_name
   # })


