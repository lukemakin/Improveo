from django import forms
from profiles.models import Profile


class FormUserRequiredMixin(object):

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            form.instance.author = profile
            return super(FormUserRequiredMixin, self).form_valid(form)
        else:
            # form.add_error("title", "user must be logged in")
            # form.add_error("description", "user must be logged in")
            form.add_error(None, "user must be logged in")
            return self.form_invalid(form)


class FormUserOwnerMixin(object):
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super(FormUserOwnerMixin, self).form_valid(form)
        else:
            form.add_error(None, "You have to be the owner of this post to modify it")
            return self.form_invalid(form)


