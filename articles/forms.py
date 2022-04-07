from django import forms
from .models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['author', 'title', 'image', 'content', 'tags']
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ArticleCreateForm_old(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def clean_title(self):  # clean_<field_name>
        data = self.cleaned_data
        title = data.get('title')
        queryset = Article.objects.filter(title_iexact=title)
        if queryset:
            raise forms.ValidationError('Bu title oldin kirirtilgan')

        # if title.lower() == 'new title':
        #     raise forms.ValidationError('new title deb kirita olmaysiz')
        return title

    def clean(self):

        data = self.cleaned_data
        title = data.get('title')
        content = data.get('content')
        if not title.istitle() and not content.istitle():
            # raise forms.ValidationError('Iltimos katta harf bilan kiriting')
            self.add_error('title', 'Iltimos bosh harf bilan kiriting')
            self.add_error('content', 'Iltimos bosh harf bilan yozing contentni')

        return data
