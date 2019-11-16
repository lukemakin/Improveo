from django.db import models
from reports.models import Report, ProblemReported
from profiles.models import Profile
from django.shortcuts import reverse
# from .validators import validate_ext
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid
import os


# Create your models here.

class ExamplePost(models.Model):
    name = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class PostQueryset(models.QuerySet):
    def public_only(self):
        return self.filter(problem_reported__public=True)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQueryset(self.model, using=self._db)

    def public_only(self):
        return self.get_queryset().public_only()


class Post(models.Model):
    liked = models.ManyToManyField(
        Profile, default=None, blank=True, related_name="liked")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="author")

    @property
    def num_likes(self):
        return self.liked.all().count()


class ProblemPost(Post):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True)
    problem_reported = models.ForeignKey(
        ProblemReported, on_delete=models.CASCADE)

    objects = PostManager()

    def __str__(self):
        return str(self.problem_reported.description[:50])

    def get_absolute_url(self):
        return reverse('posts:pp-detail', kwargs={'pk1': self.pk, 'pk': self.problem_reported.id})


def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/posts/img', filename)


class GeneralPost(Post):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=360)
    image = models.ImageField(upload_to=get_upload_path,
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("posts:gp-detail", kwargs={"pk": self.pk})

    def clean(self):
        if len(self.title) < 5:
            raise ValidationError("Title to short")
        return super(GeneralPost, self).clean()


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default="Like", max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(GeneralPost, on_delete=models.CASCADE)
    body = models.TextField(max_length=360)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.pk)

    class Meta:
        ordering = ("-timestamp",)





