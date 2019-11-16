from django.contrib import admin
from .models import Message
from .forms import MessageModelForm
# Register your models here.


admin.site.register(Message)
