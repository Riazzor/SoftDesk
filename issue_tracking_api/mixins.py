class IsContributorMixin:
    def is_owner_or_contributor(self, project):
        is_contributor = project.contributors.values_list('user').filter(user_id=self.request.user.user_id).exists()
        is_owner = (project.author_user is self.request.user)
        return is_contributor or is_owner
