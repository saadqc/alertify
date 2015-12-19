from Registrations.methods import random_string, send_email
from Registrations.models import User
from Registrations.modforms import *

__author__ = 'Saad'
import floppyforms.__future__ as forms


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='', widget=OtherPassField(attrs={'placeholder': u'PASSWORD', 'name': 'password1'}))
    password2 = forms.CharField(label='', widget=OtherPassField(attrs={'placeholder': u'CONFIRM PASSWORD', 'name': 'password2'}))

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  'city',
                  'gender')
        widgets = ({
                       'first_name': OtherTextField(attrs={'placeholder': u'FIRST NAME', 'name': 'first_name',
                                                           'ng_model': 'user_firstname'}),
                       'last_name': OtherTextField(attrs={'placeholder': u'LAST NAME', 'name': 'last_name',
                                                          'ng_model': 'user_lastname'}),
                       'gender_male': OtherCheckBoxField(attrs={'placeholder': u'', 'name': 'gender', 'value': 'Male',
                                                          'ng_model': 'user_gender'}),
                       'gender_female': OtherCheckBoxField(attrs={'placeholder': u'', 'name': 'gender', 'value': 'Female',
                                                'ng_model': 'user_gender'}),
                       'city': OtherTextField(attrs={'placeholder': u'CITY', 'name': 'city', 'value': '',
                                                       'ng_model': 'user_city'}),
                       'email': OtherEmailInput(attrs={'placeholder': u'EMAIL ADDRESS', 'name': 'email',
                                                       'ng_model': 'user_email'})
                   })

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        m = super(RegisterUserForm, self).save(commit=False)
        m.bearer_token = random_string(32)
        m.set_password(self.cleaned_data['password1'])
        if commit:
            m.save()
            return m

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        for fieldname in ['first_name', 'last_name', 'email', 'city', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''


# Login User Form
class LoginUserForm(forms.Form):
    email = forms.EmailField(help_text='', label='', widget=OtherEmailInput(attrs={'placeholder': 'EMAIL ADDRESS', 'name': 'email',
                                                                                   'ng_model': 'user_email'}))
    password = forms.CharField(help_text='', label='', widget=OtherPassField(attrs={'placeholder': 'PASSWORD', 'name': 'password',
                                                                                    'ng_model': 'user_password'}))

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        # run the parent validation first
        valid = super(LoginUserForm, self).is_valid()
        if not valid:
            return valid
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            self._errors['error'] = "User doesn't exist"
            return False

        if not str(self.cleaned_data['password']) == str(user.password):
            self._errors['error'] = "Invalid Password"
            return False

        # all good
        return True


class ForgotPasswordForm1(forms.Form):
    email = forms.EmailField(help_text='', label='', widget=OtherEmailInput(attrs={'placeholder': 'EMAIL ADDRESS', 'name': 'email'}))

    def is_valid(self):
        valid = super(ForgotPasswordForm1, self).is_valid()
        # check is step 1 form
        if not valid:
            return valid
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            return True
        except User.DoesNotExist:
            self._errors['error'] = "User doesn't exist"
            return False

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm1, self).__init__(*args, **kwargs)


class ForgotPasswordForm2(forms.Form):
    resetcode = forms.CharField(help_text='', label='', widget=OtherTextField(attrs={'placeholder': 'Reset Code', 'name': 'resetcode'}))
    password1 = forms.CharField(help_text='', label='', widget=OtherPassField(attrs={'placeholder': 'NEW PASSWORD', 'name': 'password1'}))
    password2 = forms.CharField(help_text='', label='', widget=OtherPassField(attrs={'placeholder': 'CONFIRM PASSWORD', 'name': 'password2'}))
    userId = None

    def is_valid(self):
        valid = super(ForgotPasswordForm2, self).is_valid()
        #check is step 1 form
        if not valid:
            return valid
        try:
            user = User.objects.get(email=int(None))
            if self.cleaned_data['resetcode'] == user.hash_pass and self.cleaned_data['password1'] == self.cleaned_data['password2']:
                return True
        except User.DoesNotExist:
            self._errors['error'] = "User doesn't exist"
            return False
        return False

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm2, self).__init__(*args, **kwargs)