from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from blog_admin.models import AlmanAdmin, AdminCategory, LikeAdmin


class ArticleListView(LoginRequiredMixin,View):
    def get(self, request):
        almanadmin = AlmanAdmin.objects.all()
        q = request.GET.get('q', '')
        if q:
            almanadmin = almanadmin.filter(title__icontains=q, )
        return render(request, 'blog_admin/blog_admin.html', {'almanadmin': almanadmin})


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AlmanAdmin
    fields = ('title', 'summary', 'body', 'photo',)
    template_name = 'blog_admin/blog_admin_edit.html'
    success_url = reverse_lazy('adminn')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AlmanAdmin
    template_name = 'blog_admin/blog_admin_delete.html'
    success_url = reverse_lazy('adminn')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AlmanAdmin
    template_name = 'blog_admin/blog_admin_list.html'
    fields = ('category','title', 'body', 'photo', )
    success_url = reverse_lazy('adminn')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user


#category views

def for_all_pages_admin(request):
    categories = AdminCategory.objects.all()
    return {"admin_category": categories}


class CategoryAdminView(LoginRequiredMixin,View):
    def get(self, request, admin_name):
        category = get_object_or_404(AdminCategory, name=admin_name)
        almanadmin = AlmanAdmin.objects.filter(category=category)
        q = request.GET.get('q', '')
        if q:
            products = almanadmin.filter(title__icontains=q)
        return render(request, "blog_admin/blog_admin.html", {'almanadmin': almanadmin, "category": category})
#end category views
#like button view
@login_required(login_url='users:login')
def like_postt(request, ):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = AlmanAdmin.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeAdmin.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect('adminn')
#end like button view