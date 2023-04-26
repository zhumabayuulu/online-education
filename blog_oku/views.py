from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView
from blog_oku.forms import TestForm, QuestionForm, EdirCommentForm, CommentModelForm
from blog_oku.models import BlogLearn, BlogLearnComment, Test, Question, CheckQuestion, CheckTest, LearnCategory, \
    TestCategory, LikeOku, LikeLearn, LikeTest


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogLearn
    fields = ('description','category')
    template_name = 'blog_oku/blog_oku_edit.html'
    success_url = reverse_lazy('okuu:learn_view')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class OkuCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = BlogLearn
    template_name = 'blog_oku/blog_oku_add.html'
    fields = ('category','image','description')
    success_url = reverse_lazy('okuu:learn_view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        return self.request.user

class BlogView(LoginRequiredMixin,View):
    def get(self, request,):

        bloglearn = BlogLearn.objects.all()
        q = request.GET.get('q',)
        if q:
            bloglearn = bloglearn.filter(description__icontains=q, )

        context = {
            'bloglearn': bloglearn,

        }

        return render(request, "blog_oku/blog_oku.html", context)


class BlogDetail(LoginRequiredMixin,View):
    def get(self, request, bloglearn_id):
        bloglearn = get_object_or_404(BlogLearn, id=bloglearn_id)
        comments = bloglearn.comments.filter(active=True)
        comment_count = comments.count()
        context = {
            'bloglearn': bloglearn,
            'comment_count': comment_count,
            'comments': comments
        }

        return render(request, 'blog_oku/blog_learn_detail.html', context)



@login_required(login_url='users:login')
def blog_learn_delete(request, bloglearn_id):
    bloglearn = get_object_or_404(BlogLearn, id=bloglearn_id)
    if request.user == bloglearn.author:
        if request.method == 'POST':
            bloglearn.delete()
            messages.info(request, 'Successfully Deleted!')
            return redirect('okuu:learn_view')
        return render(request, "blog_oku/blog_oku_delete.html", {'bloglearn': bloglearn})
    else:
        messages.error(request, 'Access danied!')
        return redirect('okuu:learn_view')



# create comments

@login_required(login_url='users:login')
def learn_comment(request, bloglearn_id):
    bloglearn = get_object_or_404(BlogLearn, id=bloglearn_id)
    if request.method == 'POST':
        BlogLearnComment.objects.create(
            author=request.user,
            bloglearn=bloglearn,
            body=request.POST['body']
        )

        messages.info(request, 'Successfully send comment!')
        return redirect('okuu:learn_detail', bloglearn_id)
    return HttpResponse('add comment')




@login_required(login_url='users:login')
def delete_learn_comment(request, bloglearn_id, comment_id, *args, **kwargs):
    comment = get_object_or_404(BlogLearnComment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        messages.info(request, 'Successfully delete comment!')
        return redirect('okuu:learn_detail', bloglearn_id)
    return redirect('okuu:learn_detail', bloglearn_id)


#end create comments
# test create

class TestView(LoginRequiredMixin,View):
    def get(self, request, category_name):
        category = get_object_or_404(TestCategory, name=category_name)
        products = Test.objects.filter(category=category)
        q = request.GET.get('q', '')
        if q:
            products = products.filter(title__icontains=q)
        return render(request, "blog_oku/test/test_list.html", {'tests': products, "category": category})


@login_required(login_url='users:login')
def testlist(request):
    tests = Test.objects.all()
    q = request.GET.get('q', '')
    if q:
        tests = tests.filter(title__icontains=q)
    return render(request,'blog_oku/test/test_list.html' , {'tests': tests})#'blog_oku/test_list.html'


@login_required(login_url='login')
def ready_to_test(request, test_id):  # теске дайар
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'blog_oku/test/ready_to_test.html', {'test': test})


@login_required(login_url='users:login')
def test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    attemps = CheckTest.objects.filter(student=request.user, test=test).count()
    if (timezone.now() >= test.start_date and timezone.now() <= test.end_date) and attemps < test.maximum_attemps:
        questions = Question.objects.filter(test=test)
        if request.method == 'POST':
            checktest = CheckTest.objects.create(student=request.user, test=test)
            for question in questions:
                given_answer = request.POST[str(question.id)]
                CheckQuestion.objects.create(checktest=checktest, question=question, given_answer=given_answer,
                                             true_answer=question.true_answer)
            checktest.save()
            return redirect('okuu:checktest', checktest.id)
        context = {'test': test, 'questions': questions}
        return render(request, 'blog_oku/test/test.html', context)
    else:
        return HttpResponse('test not Found!')


@login_required(login_url='users:login')
def checktest(request, checktest_id):
    checktest = get_object_or_404(CheckTest, id=checktest_id, student=request.user)
    return render(request, 'blog_oku/test/checktest.html', {'checktest': checktest})

#add question

@login_required(login_url='users:login')
def new_test(request):
    form = TestForm()
    if request.method=='POST':
        form = TestForm(data=request.POST)
        if form.is_valid:
            test_id = form.save(request)
            return redirect('okuu:new_question',test_id)
    return render(request,'blog_oku/test/new_test.html',{'form':form})

@login_required(login_url='users:login')
def new_question(request,test_id):
    test = get_object_or_404(Test,id=test_id)
    if test.author == request.user:
        form = QuestionForm()
        if request.method == 'POST':
            form = QuestionForm(data=request.POST)
            if form.is_valid:
                form.save(test_id)
                if form.cleaned_data['submit_and_exit']:
                    return redirect('okuu:list_test')     #okuu:index
                return redirect('okuu:new_question',test.id)
        return render(request,'blog_oku/test/new_question.html',{'form':form,'test':test})
    else:
        return HttpResponse('something went wrong')
#end add question


#category
def for_all_pages_oku(request):
    categories = LearnCategory.objects.all()
    return {"learn_category": categories}


class CategoryLearnView(LoginRequiredMixin,View):
    def get(self, request, oku_name):
        category = get_object_or_404(LearnCategory, name=oku_name)
        bloglearn = BlogLearn.objects.filter(category=category)
        q = request.GET.get('q', '')
        if q:
            bloglearn = bloglearn.filter(title__icontains=q)
        return render(request, "blog_oku/test/blog_oku.html", {'bloglearn': bloglearn, "category": category})

def for_all_pages_test(request):
    categories = TestCategory.objects.all()
    return {"test_category": categories}

#end category
# create like button

@login_required(login_url='users:login')
def like_learn_comment(request ,):
    user = request.user
    if request.method =='POST':
        post_id = request.POST.get('post_id')
        post_obj = BlogLearnComment.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeLearn.objects.get_or_create(user=user ,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='users:login')
def like_learn_detail(request ,):
    user = request.user
    if request.method =='POST':
        post_id = request.POST.get('pos_id')
        post_obj = BlogLearn.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeOku.objects.get_or_create(user=user ,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='users:login')
def like_test(request ,):
    user = request.user
    if request.method =='POST':
        post_id = request.POST.get('post_id')
        post_obj = Test.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeTest.objects.get_or_create(user=user ,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect('okuu:list_test',)


@login_required(login_url='users:login')
def like_oku(request ,):
    user = request.user
    if request.method =='POST':
        post_id = request.POST.get('post_id')
        post_obj = BlogLearn.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeOku.objects.get_or_create(user=user ,post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect('okuu:learn_view')

# end create like button