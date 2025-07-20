from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Message, Role, User
from .forms import MessageForm
import re

# ✅ API to return mentionable users below the current user's role
@login_required
def mentionable_users(request):
    user = request.user
    if not user.role:
        return JsonResponse([], safe=False)

    users = User.objects.filter(role__hierarchy_level__lt=user.role.hierarchy_level).exclude(id=user.id)
    data = [{'id': u.id, 'username': u.username} for u in users]
    return JsonResponse(data, safe=False)

# ✅ Main chat view
@login_required
def chat_view(request):
    user = request.user
    user_role = user.role

    # If user has no role, show error page
    if not user_role:
        return render(request, 'chat/no_role.html', {
            'message': 'You do not have a role assigned. Please contact the admin.'
        })

    # Fetch messages visible to user
    messages = Message.objects.filter(
        Q(sender=user) |
        Q(visible_to_roles=user_role) |
        Q(visible_to_users=user)
    ).distinct().order_by('timestamp')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.save()

            # Extract mentioned usernames using regex
            mentioned_usernames = re.findall(r'@([\w.@+-]+)', message.content)
            mentioned_users = User.objects.filter(username__in=mentioned_usernames)

            # Only allow tagging users *below* in hierarchy
            if user.role:
                mentioned_users = mentioned_users.filter(
                    role__hierarchy_level__lt=user.role.hierarchy_level
                )

            # Set message visibility
            message.visible_to_users.set(mentioned_users)
            message.visible_to_roles.set([user.role])
            message.save()
            return redirect('home')
    else:
        form = MessageForm()

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'form': form
    })

