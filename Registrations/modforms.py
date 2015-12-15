__author__ = 'Saad'
import floppyforms as forms


class OtherEmailInput(forms.EmailInput):
    template_name = 'mods/emailInput.html'


class OtherTextAreaField(forms.TextInput):
    template_name = 'mods/textareafield.html'

    def get_context_data(self):
        self.attrs['autofocus'] = True
        return super(OtherTextAreaField, self).get_context_data()


class OtherTextField(forms.TextInput):
    template_name = 'mods/textfield.html'

    def get_context_data(self):
        self.attrs['autofocus'] = True
        return super(OtherTextField, self).get_context_data()


class OtherPassField(forms.PasswordInput):
    template_name = 'mods/passfield.html'

    def get_context_data(self):
        self.attrs['autofocus'] = True
        return super(OtherPassField, self).get_context_data()


class OtherCheckBoxField(forms.PasswordInput):
    template_name = 'mods/checkfield.html'

    def get_context_data(self):
        self.attrs['autofocus'] = True
        return super(OtherCheckBoxField, self).get_context_data()


class OtherRadioInputField(forms.RadioSelect):
    template_name = 'mods/checkfield.html'

    def get_context_data(self):
        self.attrs['autofocus'] = True
        return super(OtherRadioInputField, self).get_context_data()
