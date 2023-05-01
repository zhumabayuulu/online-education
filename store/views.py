from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect

from accounts.models import Saved
from .forms import NewProductForm, ProductForm
from .models import ProductImage, Product, Comment, LikeStore, LikeStoreComment, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404


# Create your views here.


class IndexView(LoginRequiredMixin,View):
    def get(self, request):
        products = Product.objects.all()
        q = request.GET.get('q', '')
        if q:
            products = products.filter(Q(title__icontains=q)|Q(book_author__icontains=q))

        return render(request, "store/store.html", {'products': products,})

@login_required(login_url='users:login')
#@allowed_groups(['loki',])
def new_product(request):
    if request.method == "GET":
        form = NewProductForm()
        for f in form:
            if f.label == "Images":
                f.label = "китептин суротору"


        return render(request, 'store/product_new.html', {'form': form})
    elif request.method == "POST":
        form = NewProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(request)
            productimages = []
            for image in request.FILES.getlist("images"):
                ProductImage.objects.create(image=image, product=product)

            messages.success(request, "Successfully Created!")
            return redirect('main:shop')
        return render(request, 'store/product_new.html', {'form': form})

@login_required(login_url='users:login')
def product_updat(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user == product.author:
        if request.method == 'GET':
            form = ProductForm(instance=product)
            for f in form:
                if f.label == "Images":
                    f.label = "китептин суротору"

            return render(request, 'store/product_update.html', {'form': form, 'pr': product})
        elif request.method == 'POST':
            form = ProductForm(instance=product, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                if request.FILES.getlist('images'):
                    ProductImage.objects.filter(product=product).delete()
                    productimages = []
                    for image in request.FILES.getlist("images"):
                        productimages.append(ProductImage(image=image, product=product))
                    ProductImage.objects.bulk_create(
                        productimages
                    )
                messages.success(request, 'Successfully Updated!')
                return redirect('main:detail', product.id)
            return render(request, 'store/product_update.html', {'form': form, 'pr': product})
    else:
        messages.error(request, 'Access danied!')
        return redirect('main:shop')

@login_required(login_url='users:login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.filter(active=True)
    comment_count = comments.count()
    context = {
        'product': product,
        'comment_count': comment_count,
        'comments': comments
    }

    if "recently_viewed" in request.session:
        r_viewed = request.session["recently_viewed"]
        if not product.id in r_viewed:
            r_viewed.append(product.id)
            request.session.modified = True
    else:
        request.session["recently_viewed"] = [product.id, ]
    return render(request, 'store/product_detail.html', context)

@login_required(login_url='users:login')
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user == product.author:
        if request.method == 'POST':
            product.delete()
            messages.info(request, 'Successfully Deleted!')
            return redirect('main:shop')
        return render(request, "store/product_delete.html", {'product': product})
    else:
        messages.error(request, 'Access danied!')
        return redirect('main:shop')

@login_required(login_url='users:login')
def new_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        Comment.objects.create(
            author=request.user,
            product=product,
            body=request.POST['body']
        )

        messages.info(request, 'Successfully send comment!')
        return redirect('main:detail', product_id)
    return HttpResponse('add comment')

@login_required(login_url='users:login')
def delete_comment(request, product_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        messages.info(request, 'Successfully delete comment!')
        return redirect('main:detail', product_id)
    return redirect('main:detail', product_id)

# category
def for_all_pages(request):
    categories = Category.objects.all()
    return {"categories": categories}

class CategoryView(View):
    def get(self, request, category_name):
        category = get_object_or_404(Category, name=category_name)
        products = Product.objects.filter(category=category)
        q = request.GET.get('q', '')
        if q:
            products = products.filter(title__icontains=q)
        return render(request, "store/store.html", {'products': products, "category": category})

# end category

# like buttons
@login_required(login_url='users:login')
def like_store(request, ):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Product.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeStore.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect('main:shop')

@login_required(login_url='users:login')
def like_store_comment(request, ):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Comment.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeStoreComment.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect(request.META.get('HTTP_REFERER'))
