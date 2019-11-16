from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from django.shortcuts import reverse
from django.db.models import Q
# Create your models here.

class MessageQueryset(models.QuerySet):
    def get_all_main_user_messages(self, user):
       return self.filter(Q(message_to__user__username=user, main=True) | Q(message_from=user, main=True))

    def get_all_user_messages(self, user):
       return self.filter(message_to__user__username=user) 

    def get_read_only_messages(self):
        return self.filter(read=True)

    def get_unread_only_messages(self):
        return self.filter(read=False)


class MessageManager(models.Manager):
    def get_queryset(self):
        return MessageQueryset(self.model, using=self._db)

    def get_all_main_user_messages(self, user):
        return self.get_queryset().get_all_main_user_messages(user)

    def get_all_user_messages(self, user):
        return self.get_queryset().get_all_user_messages(user) 

    def get_read_receiver_only_messages(self):
        return self.get_queryset().get_read_only_messages()

    def get_unread_only_messages(self):
        return self.get_queryset().get_unread_only_messages()


class Message(models.Model):
    message_to = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    message_from = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    # file
    answers = models.ManyToManyField("self", blank=True, default=None)
    main = models.BooleanField(default=True)
    read = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("messages:message-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ('-timestamp',)
