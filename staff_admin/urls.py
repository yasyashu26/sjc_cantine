from django.urls import path
from staff_admin import views

urlpatterns = [
    path('staff_admin/home/', views.admin_home, name='admin_home'),
    path('staff_admin/home/Inventory/', views.inventory_mgmt, name='inventory_mgmt'),
    path('staff_admin/home/Awaited-orders/',views.awaited_orders,name='awaited_orders'),
    path('staff_admin/home/Order-paid/<int:pk>/', views.order_paid_btn, name='order_paid_btn'),   
    path('staff_admin/home/Order-Cancelled/<int:pk>/', views.order_cancelled_btn, name='order_cancelled_btn'),
    path('staff_Admin/home/Order-Paid-all/', views.all_paid_orders, name='all_paid_orders'),
    path('staff_Admin/home/Order-Served/<int:pk>/', views.order_delivered_btn, name='order_delivered_btn'),
    path('search/', views.search, name='search'),
    path('search-paidorder/', views.search_po, name='search_po'),
    path('staff_admin/home/Inventory/Add-items/', views.add_items, name='add_items'), 
    path('staff_admin/home/Inventory/Delete-items/<int:pk>/', views.delete_items, name='delete_items'),
    path('staff_admin/home/Inventory/Edit-items/<int:pk>/', views.edit_item, name='edit_item'),
    path('staff_admin/home/Inventory/Available/<int:pk>/', views.available, name='available'),
    path('staff_admin/home/Inventory/Not-Available/<int:pk>/', views.not_available, name='not_available'),
    path('staff_admin/home/order/total_served-order/', views.show_total_orders, name='show_total_orders')
]
