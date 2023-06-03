from django.contrib import admin
from .models import Banner,Category,Occasion,Size,Product,ProductAttribute,CartOrder,CartOrderItms,ProductReview,Wishlist

#admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Occasion)
admin.site.register(Size)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text','img')
admin.site.register(Banner,BannerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','occasion','status','is_featured')
    list_editable =('status','is_featured')
admin.site.register(Product,ProductAdmin)

#Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id','product','price','size')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	#list_editable=('paid_status',)
	list_display=('user','total_amt','paid_status','order_dt')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItmsAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'item', 'image_tag', 'qty', 'price', 'total', 'username')

admin.site.register(CartOrderItms, CartOrderItmsAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)