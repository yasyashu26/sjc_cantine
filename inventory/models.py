from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm

#product category
class Category(models.Model):
    title = models.CharField(max_length=300)
    primaryCategory = models.BooleanField(default=False)
    picture =  models.ImageField(upload_to='inventory/images/', blank=False)
    detail = models.TextField(max_length=200, verbose_name='Detail')
    def __str__(self):
        return self.title


#Product Model
class  Product(models.Model):
    mainimage = models.ImageField(upload_to='inventory/images/', blank=False)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=200, verbose_name='Detail Text')
    price = models.FloatField()
    available = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name


#cart model
User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)
    served = models.BooleanField(default=False)
    served_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):        
        return '{}{}{}{}{}'.format(self.quantity,' ',self.item.name,' of ₹ ',self.item.price * self.quantity)

    # Getting the total price 
    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal

# Order Model
class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    total_price=models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.CharField(max_length=5, default='null')   #yes no
    delivered =models.CharField(max_length=5, default='null') #yes no

    def __str__(self):
        return self.user.username


    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        
        return total
    
    def get_all_order(self):
        return ",".join([str(p) for p in self.orderitems.all()])



class total_order(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_items = models.IntegerField(default=0)

    def __str__(self):
        return self.item.name

