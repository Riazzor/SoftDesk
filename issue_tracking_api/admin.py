from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
    )


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "created_time",
    )


@admin.register(models.Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
        "permission",
        "role",
    )


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "tag",
        "status",
        "assignee",
        "created_time",
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author_user",
        "issue",
        "created_time",
    )
