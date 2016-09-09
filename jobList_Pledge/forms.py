

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {

        }