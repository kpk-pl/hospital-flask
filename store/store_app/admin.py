from django.contrib import admin
from store_app.models import *

admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)