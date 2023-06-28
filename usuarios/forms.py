from django import forms

class LoginForms(forms.Form):

    nome_login = forms.CharField(
        label="Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-4",
                "placeholder": "nome@exemplo.com"
            }
        )
    )
    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-4",
                "placeholder": "Sua Senha"
            }
        )
    )

class CadastroForms(forms.Form):

    nome_cadastro = forms.CharField(
        label="Seu nome completo",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-4",
                "placeholder": "Ex: João Silva"
            }
        )
    )
    email_cadastro = forms.CharField(
        label="Seu Email",
        required=True,
        max_length=70,
        widget=forms.EmailInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-4",
                "placeholder": "nome@exemplo.com"
            }
        )
    )