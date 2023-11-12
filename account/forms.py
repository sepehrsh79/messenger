from django import forms

from account.models import CustomUser


class LoginUser(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput())


class SaveUser(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'bio', 'avatar')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password.isdigit() or len(password) < 7:
            raise forms.ValidationError('کلمه عبور باید بیشتر از 7 کارکتر و شامل حروف و اعداد باشد!')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        re_password = self.cleaned_data.get('password2')
        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند!')
        return password


class UpdateProfile(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'avatar',)

