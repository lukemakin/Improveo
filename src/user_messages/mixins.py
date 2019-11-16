from django import forms
from profiles.models import Profile
from django.contrib import messages


class FormValidationMixin(object):

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.message_to == profile:
            form.add_error('message_to', "Can't send a message to yourself")
            return self.form_invalid(form)
        else:
            form.instance.message_from = self.request.user
            messages.info(self.request, "Message send")
            return super().form_valid(form)
