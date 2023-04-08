from django import forms

from blog_oku.models import Test, Question, BlogLearnComment


class EdirCommentForm(forms.ModelForm):
    class Meta:
        model = BlogLearnComment
        fields = ( 'body',)

class CommentModelForm(forms.ModelForm):
    #model = BlogLearnComment
    #fields = ['body']
    body = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = BlogLearnComment
        fields = ('body',)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title','category','maximum_attemps','start_date',"end_date",'pass_percentage')

    def save(self,request,commit=True):
        test = self.instance
        test.author = request.user
        super().save(commit)
        return test.id

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','a','b','c','d','true_answer')
    submit_and_exit = forms.BooleanField(required=False)

    def save(self,test_id,commit=True):
        question = self.instance
        question.test = Test.objects.get(id=test_id)
        super().save(commit)
        return question
