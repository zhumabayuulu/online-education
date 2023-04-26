
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import Friend, CustomUser
from .models import Chat

@login_required(login_url='users:login')
def chat(request, username):
    receiver = CustomUser.objects.get(username=username)
    user = request.user
    friends = set(Friend.objects.filter(user=user))
    friend = CustomUser.objects.filter(username__in=friends)

    # Send massage
    if request.method == "POST":
        massage = request.POST['massage']
        chat = Chat(chat=massage, sender=user, receiver=receiver)
        chat.save()
        try:
            Friend.objects.get(user=user, friend=receiver)
        except Friend.DoesNotExist:
            Friend.objects.create(user=user, friend=receiver)
            Friend.objects.create(user=receiver, friend=user)

    # List of Friends
    for f in friend:
        unread = Chat.objects.filter(sender=f, receiver=user, is_seen="&#10003;").count()
        fr = Friend.objects.filter(user=user, friend=f)
        fr.update(unread=unread)

    return render(request, 'chat/chat.html', {'receiver': receiver, 'friends': friends})


@login_required(login_url='users:login')
def data(request, username):
    receiver = CustomUser.objects.get(username=username)
    sender = user = request.user
    massages = Chat.objects.filter(
        Q(receiver=receiver, sender=sender) | Q(receiver=sender, sender=receiver)
    ).order_by("id")
    Chat.objects.filter(sender=receiver, is_seen="&#10003;").update(is_seen="&#10003; &#10003;")
    # Equilize unred to 0 when user see the massages

    fr = Friend.objects.filter(user=user, friend=receiver)
    fr.update(unread=0)
    return JsonResponse({"massages": list(massages.values())})


@login_required(login_url='users:login')
def friends(request):
    user = request.user
    friends = set(Friend.objects.filter(user=user))
    friend = CustomUser.objects.filter(username__in=friends)
    for f in friend:
        unread = Chat.objects.filter(sender=f, receiver=user, is_seen="&#10003;").count()
        fr = Friend.objects.filter(user=user, friend=f)
        fr.update(unread=unread)
    return render(request, 'chat/home_chat.html', {'friends': friends})