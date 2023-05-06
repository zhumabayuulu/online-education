
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from blog_admin.models import AlmanAdmin
from blog_nature.models import Nature
from blog_oku.models import BlogLearn, Test
from store.models import Product
from .forms import CustomUserCreationForm, CustomUserChangeForm, ContactFormm
from .models import CustomUser, Saved, SavedNature, SavedAdmin, SavedLearn, Friend, SavedTest
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.


class SignupView(UserPassesTestMixin, View):
    def get(self, request):
        if request.method == "GET":
            form = CustomUserCreationForm()
            for f in form:
                if f.label == "Password":
                    f.label = "китептин суротору"
        return render(request, 'registration/signup.html', {'forms': CustomUserCreationForm()})

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)


        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            form.save()
            messages.success(request, 'Your account is successfully created.')
            return redirect('users:login')
        else:
            messages.info(request, "Document deleted.")
        return render(request, 'registration/signup.html', {'forms': form})

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        return True

class Login(View):
    def get(self,request):
        login_form = AuthenticationForm(data=request.POST)

        return render(request, 'registration/login.html', {'form': login_form})

    def post(self,request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request,user)

            return redirect('adminn')
        else:
            return render(request, 'registration/login.html', {'form': login_form})

@login_required
def profile(request, username):
    user = CustomUser.objects.get(username=username)
    friends = set(Friend.objects.filter(user=user))
    is_owner = False

    if user == request.user:
        is_owner = True

    print(is_owner)
    return render(request, 'registration/profile.html', {"user": user,'friends':friends})


def logout_user(request):
    logout(request)
    return render(request, 'home.html', )
   # return redirect('signup')




class ProfailView( LoginRequiredMixin,View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        #return render(request, 'registration/profile.html',{'customuser': user})
        return render(request,'registration/profile.html', {'customuser': user})

class UpdateProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'registration/profile_update.html', {'form': form})

    def post(self, request):
        form = CustomUserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully updated.')
            return redirect('users:profile', request.user)
        return render(request, 'registration/signup.html', {'form': form})


class RecentlyViewedView(LoginRequiredMixin,View):
    def get(self, request):
        if not "recently_viewed" in request.session:
            products = []
        else:
            r_viewed = request.session["recently_viewed"]
            products = Product.objects.filter(id__in=r_viewed)
            q = request.GET.get('q', '')
            if q:
                products = products.filter(title__icontains=q)
        return render(request, "store/recently_viewed.html", {'products': products})

# nature saveds
class NatureSavedView(LoginRequiredMixin,View):
    def get(self, request, nature_id):
        nature = get_object_or_404(Nature, id=nature_id)
        saved_nature = SavedNature.objects.filter(author=request.user, nature=nature)
        if saved_nature:
            saved_nature.delete()
            messages.success(request, 'очурулду.')
        else:
            SavedNature.objects.create(author=request.user, nature=nature)
            messages.success(request, 'сакталды.')
        return redirect(request.META.get('HTTP_REFERER'))

class AdminSavedView(LoginRequiredMixin,View):
    def get(self, request, admin_id):
        almanadmin = get_object_or_404(AlmanAdmin, id=admin_id)
        saved_admin = SavedAdmin.objects.filter(author=request.user, almanadmin=almanadmin)
        if saved_admin:
            saved_admin.delete()
            messages.success(request, 'очурулду.')
        else:
            SavedAdmin.objects.create(author=request.user, almanadmin=almanadmin)
            messages.success(request, 'сакталды.')
        return redirect(request.META.get('HTTP_REFERER'))


class LearnSavedView(LoginRequiredMixin,View):
    def get(self, request, bloglearn_id):
        bloglearn = get_object_or_404(BlogLearn, id=bloglearn_id)
        saved_learn = SavedLearn.objects.filter(author=request.user, bloglearn=bloglearn)
        if saved_learn:
            saved_learn.delete()
            messages.success(request, 'очурулду.')
        else:
            SavedLearn.objects.create(author=request.user, bloglearn=bloglearn)
            messages.success(request, 'сакталды.')
        return redirect(request.META.get('HTTP_REFERER'))


class AddRemoveSavedView(LoginRequiredMixin,View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        saved_product = Saved.objects.filter(author=request.user, product=product)
        if saved_product:
            saved_product.delete()
            messages.success(request, 'очурулду.')
        else:
            Saved.objects.create(author=request.user, product=product)
            messages.success(request, 'сакталды')
        return redirect(request.META.get('HTTP_REFERER'))


class TestSavedView(LoginRequiredMixin,View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        saved_test = SavedTest.objects.filter(author=request.user, test=test)
        if saved_test:
            saved_test.delete()
            messages.success(request, 'очурулду.')
        else:
            SavedTest.objects.create(author=request.user, test=test)
            messages.success(request, 'сакталды')
        return redirect(request.META.get('HTTP_REFERER'))


class SavedView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        saveds = Saved.objects.filter(author=request.user, )
        testsaveds = SavedTest.objects.filter(author=request.user, )
        savedss = SavedNature.objects.filter(author=request.user, )
        saveds_learn = SavedLearn.objects.filter(author=request.user, )
        saveds_admin = SavedAdmin.objects.filter(author=request.user, )
        context ={
            "saveds": saveds,
            "savedss": savedss,
            'learn':saveds_learn,
            'saveds_admin':saveds_admin,
            'testsaveds':testsaveds,
        }
        return render(request, 'saveds.html', context)
@login_required
def contactForm(request):
    form = ContactFormm(request.POST,)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "биз менен байланышка чыканынызга рахмат адистер сиз менен байланышат")
        return redirect("adminn")
    return render(request,'registration/contact_form.html')

@login_required
def discover(request):
    if 'q' in request.GET:
        q = request.GET['q']
        users = CustomUser.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)).order_by("-last_login")
    else:
        users = CustomUser.objects.all().order_by('-last_login')

    return render(request, 'chat/discover.html', {'users': users})

