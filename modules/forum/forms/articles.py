from django import forms
from modules.forum.models import Article
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from forum_project import settings

class ArticleCreateForm(forms.ModelForm):

    # recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
    #                            private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')

    class Meta:
        model = Article
        fields = (
            'title',
            'slug',
            'category',
            'short_description',
            'full_description',
            'thumbnail',
            'meta_title',
            'meta_keywords',
            'meta_description',
            'is_published',
            'tags'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
            self.fields['meta_title'].widget.attrs.update({
                'placeholder': 'Meta tiêu đề'
            })
            self.fields['title'].widget.attrs.update({
                'placeholder': 'Tiêu đề'
            })
            self.fields['slug'].widget.attrs.update({
                'placeholder': 'URL của bài đăng (có thể bỏ trống)'
            })
            self.fields['meta_description'].widget.attrs.update({
                'placeholder': 'Meta mô tả'
            })
            self.fields['meta_keywords'].widget.attrs.update({
                'placeholder': 'Meta từ khóa'
            })
            self.fields['category'].empty_label = 'Chọn một thể loại'
            self.fields['is_published'].widget.attrs.update({
                'class': 'form-check-input'
            })
            self.fields['full_description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})            
            self.fields['full_description'].required = False

class ArticleUpdateForm(ArticleCreateForm):
    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields + ('reason', 'is_fixed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_fixed'].widget.attrs.update({
                'class': 'form-check-input'
        })