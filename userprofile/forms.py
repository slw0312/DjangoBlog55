# 引入表单类
from django import forms
# 引入User类
from django.contrib.auth.models import User
# 引入Profile模型
from .models import Profile


# 登录表单，继承forms.Form类(适用于不与数据库进行直接交互的功能)
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单,继承forms.ModelForm类(适合于需要直接与数据库交互的功能)
class UserRegisterForm(forms.ModelForm):
    # 复写User的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data  # 对单个字段的数据进行验证清洗
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重试。')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
