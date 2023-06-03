from .models import Product,ProductAttribute
def get_filters(request):
    cats=Product.objects.distinct().values('category__title','category__id')
    occasions=Product.objects.distinct().values('occasion__title','occasion__id')
    sizes=ProductAttribute.objects.distinct().values('size__title','size__id')
    data={
            'cats':cats,
            'occasions':occasions,
            'sizes':sizes,
        }
    return data