from django import forms
from modules.forum.models import Comment


class CommentCreateForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Thêm bình luận', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)