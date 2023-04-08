
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.mixins import AllowedGroupsMixin
from accounts.models import CustomUser, SavedNature
from blog_nature.forms import NatureForm
from blog_nature.models import Nature, NatureCategory, Like

@login_required(login_url='users:login')
def NatureView(request ,):
    products = Nature.objects.all()
    savedss = SavedNature.objects.filter(author=request.user, )
    q = request.GET.get('q', '')
    if q:
        products = products.filter(address__icontains=q, )
    return render(request, "blog_nature/blog_nature.html", {'products': products,'savedss':savedss})


class NatureCreateView(AllowedGroupsMixin,LoginRequiredMixin, UserPassesTestMixin, CreateView):
    allowed_groups = ['loki',]
    model = Nature
    template_name = 'blog_nature/blog_nature_add.html'
    fields = ('category', 'image', 'video','address',)
    success_url = reverse_lazy('nature:nature')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user

@login_required(login_url='users:login')
def nature_update(request, nature_id):
    nature = get_object_or_404(Nature, id=nature_id)
    if request.user == nature.author:
        if request.method == 'GET':
            form = NatureForm(instance=nature)
            return render(request, 'blog_nature/blog_nature_update.html', {'form': form, 'pr': nature})
        elif request.method == 'POST':
            form = NatureForm(instance=nature, data=request.POST,)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Updated!')
                return redirect('nature:nature',)
            return render(request, 'blog_nature/blog_nature_update.html', {'form': form,})
    else:
        messages.error(request, 'Access danied!')
        return redirect('nature:nature')

#delete
@login_required(login_url='users:login')
def nature_delete(request, product_id):
    nature = get_object_or_404(Nature, id=product_id)
    if request.user == nature.author:
        if request.method == 'POST':
            nature.delete()
            messages.info(request, 'Successfully Deleted!')
            return redirect('nature:nature')
        return render(request, "blog_nature/blog_nature_delete.html", {'nature': nature})
    else:
        messages.error(request, 'Access danied!')
        return redirect('nature:nature')
#end delete
# category

def for_all_pages_nature(request):
    categories = NatureCategory.objects.all()
    return {"nature_category": categories}


class CategoryNatureView(LoginRequiredMixin,View):
    def get(self, request, nature_name):
        category = get_object_or_404(NatureCategory, name=nature_name)
        products = Nature.objects.filter(category=category)
        q = request.GET.get('q', '')
        if q:
            products = products.filter(title__icontains=q)
        return render(request, "blog_nature/blog_nature.html", {'products': products, "category": category})

#end category
#like button
@login_required(login_url='users:login')
def like_post(request ,):
    user = request.user
    if request.method =='POST':
        post_id = request.POST.get('post_id')
        post_obj = Nature.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user ,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect('nature:nature')

#end like button