class IsOwnerOrContributorMixin:
    def is_owner(self, project):
        return (project.author_user == self.request.user)

    def is_owner_or_contributor(self, project):
        is_contributor = project.contributors.values_list('user').filter(user_id=self.request.user.user_id).exists()
        return is_contributor or self.is_owner(project)
