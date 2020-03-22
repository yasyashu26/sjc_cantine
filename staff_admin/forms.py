from django.forms import ModelForm
from inventory.models import Product

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ['mainimage', 'name', 'category', 'preview_text', 'detail_text', 'price']
    
