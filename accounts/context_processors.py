from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from store.models import Category


def for_all_pages(request):
    categories = Category.objects.all()
    return {"categories":categories}
