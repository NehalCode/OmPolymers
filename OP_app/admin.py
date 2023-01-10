from django.contrib import admin
from OP_app.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Product_category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)