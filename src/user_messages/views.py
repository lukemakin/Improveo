from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from .forms import MessageModelForm, MessageAnswerModelForm
from .models import Message
from profiles.models import Profile
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .mixins import FormValidationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.


class MessageCreateView(LoginRequiredMixin, FormValidationMixin, CreateView):
    model = Message
    form_class = MessageModelForm
    template_name = "user_messages/new_message.html"
    success_url = reverse_lazy('messages:message-write')

    def form_invalid(self, form):
        messages.warning(self.request, "There was an error..")
        return super().form_invalid(form)


class GeneralListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "user_messages/view_messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["read_receiver"] = Message.objects.get_all_main_user_messages(
            self.request.user).get_read_only_messages()

        context["unread_receiver"] = Message.objects.get_all_user_messages(
            self.request.user).get_unread_only_messages().distinct().count()
        return context


class MessagesListAll(GeneralListView):

    def get_queryset(self):
        qs = Message.objects.get_all_main_user_messages(self.request.user)
        return qs


class MessageDetail(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "user_messages/detail_message.html"

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(user=self.request.user)
        message = get_object_or_404(Message, pk=pk, main=True)
        
        if message.answers.all().count() > 0:
            ml = message.answers.filter(main=False, message_to=profile)
            for m in ml:
                if m.read == False:
                    m.read = True
                    m.new = False
                    m.save()
                    message.new = False
                   

        if message.message_to == profile:
            if message.read == False:
                message.read = True
                message.new = False


        message.save()
        return message

    def get_context_data(self, **kwargs):
        form = MessageAnswerModelForm()
        context = super().get_context_data(**kwargs)
        context["form"] = MessageAnswerModelForm()
        return context

    def post(self, *args, **kwargs):
        message = self.get_object()
        profile = Profile.objects.get(user=self.request.user)
        profile_from = Profile.objects.get(user__username=message.message_from)
        profile_to = Profile.objects.get(user__username=message.message_to)
        form = MessageAnswerModelForm(self.request.POST or None)

        if form.is_valid():
            instance = form.save(commit=False)
            if message.message_to == profile:
                instance.message_to = profile_from
                instance.message_from = profile_to
            else:
                instance.message_to = profile_to
                instance.message_from = profile_from

            instance.title = message.title
            instance.main = False
            instance.body = form.cleaned_data.get('body')
            form.save()
            message.answers.add(instance)
            message.new = True
            message.save()
        return redirect(self.request.META.get('HTTP_REFERER'))
        # return redirect('messages:message-list')
