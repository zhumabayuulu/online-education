from .models import Product
from django import forms


class NewProductForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Product
        fields = ( 'category','title',"description",'book_author','pdf', 'price', "language")
        labels = {'category':'болум',
                  'title':' китептин аты',
                  "description":'китеп жонундо малымат жазыныз',
                  'book_author':"Китептин авторлор:",
                  'price':"Басы:(эгер бекер болсо жазу шарт эмес)",
                  "language":"китеп жазылган тил",
                  "images":"суротору",
        }


    def save(self, request, commit=True):
        product = self.instance
        product.author = request.user
        super().save(commit)
        return product


class ProductForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Product
        fields = ('category','title', 'price','book_author', 'pdf',)
        labels = {'category': 'болум',
                  'title': ' китеп жонундо кичине малымат',
                  "description": 'китеп жонундо малымат',
                  'book_author': "китептин автору",
                  'price': "басы эгер бекер болсо жазуу шарт эмес",
                  "images": "суротору",
                  }
