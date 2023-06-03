from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
#Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)
  

def image_tag(self):
    return mark_safe('<img src="%s" width="100" />') % (self.image.url)

def __str__(self):
        return self.alt_text

#Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.title
    

#occasion
class Occasion(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="occasion_imgs/")

    def __str__(self):
        return self.title


#Size    
class Size(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title


#Product model
class Product(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="occasion_images/")
    slug=models.CharField(max_length=400)
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    occasion=models.ForeignKey(Occasion,on_delete=models.CASCADE)
    #size=models.ForeignKey(Size,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
#Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveBigIntegerField()
    
    def __str__(self):
        return self.product.title
    

#order
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)

class CartOrderItms(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    @property
    def username(self):
        return self.order.user.username

#productreview
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     review_text=models.TextField()
     review_rating=models.CharField(choices=RATING,max_length=150)

     def get_review_rating(self):
         return self.review_rating
     
#wishlist
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

