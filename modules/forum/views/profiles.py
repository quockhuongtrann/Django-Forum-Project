from django.views.generic import DetailView, UpdateView
from modules.forum.models import Profile
from modules.forum.forms.profiles import ProfileUpdateForm, UserUpdateForm
from django.db import transaction
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse

class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'modules/forum/profiles/profile_detail.html'
    # queryset = model.objects.detail()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hồ sơ cá nhân của {self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'modules/forum/profiles/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Cập nhật hồ sơ cá nhân của: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug': self.object.slug})

class ProfileFollowingCreateView(View):
    model = Profile

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, slug):
        if self.is_ajax():
            user = self.model.objects.get(slug=slug)
            current_user = request.user
            if current_user.is_authenticated:
                profile = current_user.profile
                if profile in user.followers.all():
                    user.followers.remove(profile)
                    return JsonResponse({
                        'author': current_user.username,
                        'following_avatar': profile.get_avatar,
                        'following_get_absolute_url': profile.get_absolute_url(),
                        'following_slug': profile.slug,
                        'message': f'Subscribe {user}',
                        'status': False},
                    status=200)
                else:
                    user.followers.add(profile)
                    return JsonResponse({
                        'author': current_user.username,
                        'following_avatar': profile.get_avatar,
                        'following_get_absolute_url': profile.get_absolute_url(),
                        'following_slug': profile.slug,
                        'message': f'Unsubscribe {user}',
                        'status': True},
                        status=200)
            else:
                return JsonResponse({'error': 'Yêu cầu đăng nhập'}, status=400)