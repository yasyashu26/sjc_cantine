from django.contrib import admin
from inventory.models import Category, Product, Cart,Order, total_order

class Productadmin(admin.ModelAdmin):
    list_display = ['pk','name','price','mainimage','category','preview_text','detail_text', 'available']
    class meta:
        model=Product

class Categoryadmin(admin.ModelAdmin):
    list_display = ['pk','title','picture','detail','primaryCategory']
    class meta:
        model=Category

class Cartadmin(admin.ModelAdmin):
    list_display = ['pk','user','item','quantity','created','purchased','served','served_date']
    class meta:
        model=Cart

class Orderadmin(admin.ModelAdmin):
    list_display = ['pk','user','get_all_order','total_price','created','ordered','paid', 'delivered']
    
    class meta:
        model=Order

class total_orderadmin(admin.ModelAdmin):
    list_display = ['pk','item','total_items']
    class meta:
        model=total_order


admin.site.register(Category, Categoryadmin)
admin.site.register(Product, Productadmin)
admin.site.register(Cart, Cartadmin)
admin.site.register(Order, Orderadmin)
admin.site.register(total_order, total_orderadmin)
