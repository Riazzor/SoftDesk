from rest_framework import serializers

from . import models


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = models.User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["project_id", "title", "description", "type", "created_time", "updated_time"]
        read_only_fields = ["created_time", "updated_time"]


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="email", queryset=models.User.objects.all())

    class Meta:
        model = models.Contributor
        fields = ["user", "project", "permission", "role"]
        read_only_fields = ["project"]
        depth = 1

    def validate(self, attrs):
        if models.Contributor.objects.filter(
            user=attrs['user'],
            project__project_id=self.context.get('project_pk'),
        ):
            raise serializers.ValidationError('Contributor already exist')
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["project"] = data["project"]["title"]
        return data


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = ["issue_id", "title", "description", "tag", "priority", "project", "status", "author_user", "assignee"]
        read_only_fields = ["project", "created_time", "updated_time"]
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author_user"] = data["author_user"]["username"]
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["comment_id", "description", "author_user", "issue", "created_time", "updated_time"]
        read_only_fields = ["issue", "created_time", "updated_time"]
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author_user"] = data["author_user"]["username"]
        return data
