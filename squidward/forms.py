from django import forms


class SquidReportIndex(forms.Form):
    """

    """
    date_start = forms.DateField(label='Начало:',
                                 input_formats=['%m/%d/%Y'],
                                 )

    date_stop = forms.DateField(label='Конец:',
                                 input_formats=['%m/%d/%Y'])


class Login(forms.Form):
    """
    Simple login form
    """
    # login = forms.TextInput(label='Имя пользователя:')
    login = forms.CharField(label="Логин: ")
    # password = forms.PasswordInput(label='Пароль:', widget=forms.PasswordInput)
    password = forms.CharField(label="Пароль: ", widget=forms.PasswordInput())


class PPTP(forms.Form):
    """

    """

    ipaddress = forms.CharField(label='IP адрес')
    date_start = forms.DateField(label='Начало', input_formats=['%m/%d/%Y'])
    date_stop = forms.DateField(label='Конец', input_formats=['%m/%d/%Y'])
