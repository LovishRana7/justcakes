from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Occasion,Product,ProductAttribute,CartOrderItms,CartOrder,ProductReview,Wishlist
from django.template.loader import render_to_string
from .forms import SignupForm,ReviewAdd
from django.db.models import Avg
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
#Home Page
def home(request):
    banners=Banner.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=True).order_by('-id')
    return render(request,'index.html',{'data':data,'banners':banners})

#For Searchimg
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q,).order_by('-id')
    return render(request,'search.html',{'data':data,})

#category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

#Occasion
def occasion_list(request):
    data=Occasion.objects.all().order_by('-id')
    return render(request,'occasion_list.html',{'data':data})

# Product List

def product_list(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:6]
    #min_price=ProductAttribute.objects.aggregate(Min('price'))
    #max_price=ProductAttribute.objects.aggregate(Max('price'))   
    return render(request,'product_list.html',
        {
            'data':data,
            'total_data':total_data,
           # 'min_price':min_price,
            #'max_price':max_price,
            
        }
        )

#Product List according to Category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    return render(request,'category_product_list.html',{
            'data':data,
        }
        )

#Product List according to Occasion
def occasion_product_list(request,occasion_id):
    occasion=Occasion.objects.get(id=occasion_id)
    data=Product.objects.filter(occasion=occasion).order_by('-id')
    return render(request,'category_product_list.html',{
            'data':data,
        }
        )


#Product detail
def product_detail(request,slug,id):
    product=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price').distinct()
    reviewForm=ReviewAdd()

    reviews=ProductReview.objects.filter(product=product)
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))


    return render(request,'product_detail.html',{'data':product,'related':related_products,'sizes':sizes,'reviewForm':reviewForm,'reviews':reviews,'avg_reviews':avg_reviews})

#filter data
def filter_data(request):
    categories=request.GET.getlist('category[]')
    occasions=request.GET.getlist('occasion[]')
    sizes=request.GET.getlist('size[]')
	#minPrice=request.GET['minPrice']
	#maxPrice=request.GET['maxPrice']
    allProducts=Product.objects.all().order_by('-id').distinct()
   # allProducts=allProducts.filter(productattribute__price__gte=minPrice)
   # allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
    if len(categories)>0:
    	allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(occasions)>0:
    	allProducts=allProducts.filter(occasion__id__in=occasions).distinct()
    if len(sizes)>0:
    	allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('ajax/product-list.html',{'data':allProducts})
    return JsonResponse({'data':t})


#load more data
def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    data=Product.objects.all().order_by('-id')[offset:offset+limit]   
    t=render_to_string('ajax/product-list.html',{'data':data})
    return JsonResponse({'data':t})


#add to cart
def add_to_cart(request):
    #del request.session['cartdata']
    cart_p={}
    cart_p[str(request.GET['id'])]={
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty']) 
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

#Cart list page
def cart_list(request):
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
   

# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

#delete cart item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# Signup Form
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


# Checkout
@login_required
def checkout(request):
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			totalAmt+=int(item['qty'])*float(item['price'])
		# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# OrderItems
			items=CartOrderItms.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End
		
		return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})




#user dashboard
def my_dashboard(request):
     return render(request, 'user/dashboard.html')
#my orders
def my_orders(request):
     orders=CartOrder.objects.filter(user=request.user).order_by('-id')
     return render(request, 'user/orders.html',{'orders':orders})
#orderdetail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItms.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems})


#save review
def save_review(request,pid):
    product =Product.objects.get(pk=pid)
    user=request.user
    review=ProductReview.objects.create(
         user=user,
         product=product,
         review_text=request.POST['review_text'],
         review_rating=request.POST['review_rating'],
        )
    data={
         'user':user.username,
         'review_text':request.POST['review_text'],
         'review_rating':request.POST['review_rating'],
    }   
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# My Reviews
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews})

def about(request):
    return render(request, 'about.html')
def tc(request):
    return render(request, 'tc.html')

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})