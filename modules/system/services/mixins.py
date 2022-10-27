from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages
class AuthorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user != self.get_object().author:
                messages.info(request, 'Chỉ có tác giả của bài đăng được chỉnh sửa.')
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)