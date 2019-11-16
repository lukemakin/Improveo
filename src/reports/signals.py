from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProblemReported, Report
from .utils import create_problem_id
from posts.models import ProblemPost
from profiles.models import Profile


@receiver(post_save, sender=ProblemReported)
def post_save_problem_id(sender, instance, created, *args, **kwargs):
    if created:
        if instance.problem_id is None:
            instance.problem_id = create_problem_id()
            instance.save()


@receiver(post_save, sender=ProblemReported)
def post_save_report(sender, instance, created, *args, **kwargs):
    if created:
        try:
            id_ = instance.report.id
            rep = Report.objects.get(id=id_)
        except Report.DoesNotExist:
            rep = None

        if rep is not None:
            user = instance.user
            author = Profile.objects.get(user=user)
            ProblemPost.objects.create(
                author=author, report=rep, problem_reported=instance)

