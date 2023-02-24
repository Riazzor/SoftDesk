from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(verbose_name="Prénom", blank=False, max_length=128)
    last_name = models.CharField(verbose_name="Nom de famille", blank=False, max_length=128)
    email = models.EmailField(verbose_name="Adresse email", blank=False, max_length=128, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = "backend", ("Backend")
        FRONTEND = "frontend", ("Frontend")
        IOS = "ios", ("Ios")
        ANDROID = "android", ("Android")

    project_id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="Titre", blank=False, max_length=128)
    description = models.CharField(max_length=1024)
    type = models.CharField(
        max_length=128,
        choices=ProjectType.choices,
        default=ProjectType.BACKEND,
    )
    author_user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Contributor(models.Model):
    class Permissions(models.TextChoices):
        READ_ONLY = "read", _("Lecture seule")
        WRITE = "write", _("Ecriture")
        DELETE = "delete", _("Suppression")

    class Roles(models.TextChoices):
        AUTHOR = "author", _("Auteur")
        MEMBER = "member", _("Membre")
        CONTRIBUTOR = "contributor", _("Contributeur")

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )
    permission = models.CharField(
        max_length=128,
        choices=Permissions.choices,
        default=Permissions.READ_ONLY,
    )
    role = models.CharField(
        max_length=128,
        choices=Roles.choices,
    )

    class Meta:
        unique_together = ('project', 'user')  # can't assign the same user twice to the same project.


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = "bug", _("Bug")
        FEATURE = "feature", _("Amelioration")
        TASK = "task", _("Tache")

    class Priority(models.TextChoices):
        LOW = "low", _("Faible")
        MEDIUM = "medium", _("Moyen")
        HIGH = "high", _("Eleve")

    class Status(models.TextChoices):
        TODO = "todo", _("A faire")
        IN_PROGRESS = "in_progress", _("En cours")
        DONE = "done", _("Termine")

    issue_id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="Titre", blank=False, max_length=128)
    description = models.CharField(max_length=128)
    tag = models.CharField(
        verbose_name="Étiquette",
        max_length=128,
        choices=Tag.choices,
    )
    priority = models.CharField(
        verbose_name="Priorité",
        max_length=128,
        choices=Priority.choices,
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    status = models.CharField(
        max_length=128,
        choices=Status.choices,
    )
    author_user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="issues",
        null=True,
    )
    assignee = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=128)
    author_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
