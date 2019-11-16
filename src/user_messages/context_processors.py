from .models import Message

def get_unread_messages(request):
    if request.user.is_authenticated:

        qs = Message.objects.get_all_user_messages(
            request.user).get_unread_only_messages().distinct().count()
        return {"messages_undread": qs}
    return {}



