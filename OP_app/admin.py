from django.contrib import admin
from OP_app.models import *
from django.utils.html import format_html
from datetime import datetime
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.site_header ='Om polymers Admin'
admin.site.index_title ='Om polymers - Admin'


class UserAdmin(admin.ModelAdmin):
    list_display  = ("firstname", "lastname", "email")
admin.site.register(User,UserAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display  = ("name","email")
admin.site.register(Contact,ContactAdmin)

    
admin.site.register(Product_category)

class productAdmin(admin.ModelAdmin):
    list_display  = ("image","Product_name","Product_price")

    def image(self,obj):
        return format_html('<img src={} width="50" height="50" />'.format(obj.Product_image.url))
admin.site.register(Product,productAdmin)

admin.site.register(Cart)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user",)
admin.site.register(Wishlist,WishlistAdmin)


class orderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    model = Order
    # actions = ['Report_Generate']

    # def Report_Generate(self,request,queryset):
    #     today = datetime.now()
    #     data = queryset.filter(date_time__month=today.month)
    #     print(data)


    # fields = ("first_name","last_name","email","status","total_price")
    list_display  = ("first_name", "email", "total_price","status","date_time")
admin.site.register(Order,orderAdmin)


class orderitemAdmin(admin.ModelAdmin):
    list_display  = ("Order_id", "Product_id")
admin.site.register(Order_item,orderitemAdmin)


