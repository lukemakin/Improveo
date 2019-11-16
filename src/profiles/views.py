from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm
# Create your views here.


def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)
    if request.method == 'POST':
        print("test")
        if form.is_valid():
            print("test2")
            instance = form.save(commit=False)
            instance.bio = form.cleaned_data.get('bio')
            instance.profile_picture = form.cleaned_data.get('profile_picture')
            form.save()

    obj = Profile.objects.get(user=request.user)
    context = {
        'object': obj,
        'form': form,
    }
    return render(request, 'profiles/profile.html', context)


