from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
import random
import smtplib
from email.message import EmailMessage
from pathlib import os
from dotenv import load_dotenv
from django.contrib import auth
from django.contrib import messages




def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            email_login = form['email_login'].value()
            senha = form['senha'].value()

            usuario = auth.authenticate(
                request,
                email=email_login,
                password=senha
            )

            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f"{email_login} agora está logado.")
                return redirect('index')
            else:
                messages.error(request, "Erro ao efetuar Login.")
                return redirect('login')

    return render(request, "usuarios/login.html", {"form": form})


def cadastro(request):
        form = CadastroForms()

        if request.method == 'POST':
            form = CadastroForms(request.POST)

        if form.is_valid():
             nome=form["nome_cadastro"].value()
             email_cadastro=form["email_cadastro"].value()

             if User.objects.filter(username=nome).exists() or User.objects.filter(email=email_cadastro).exists():
                  print('Email ou Nome já cadastrado no sistema')
                  messages.error(request, 'Email ou Nome já cadastrado no sistema')
                  return redirect('cadastro')
             
             senha = random.sample(range(10),6)
             # concatenar(mapear(tipo,valor))
             senha_aleatoria = ''.join(map(str, senha))
             
             usuario = User.objects.create_user(
                  username=nome,
                  email=email_cadastro,
                  password=senha_aleatoria
             )

             usuario.save()
             enviar_email(nome, email_cadastro, senha_aleatoria)
             messages.success(request,'Cadastro efetuado com sucesso.')
             return redirect('login')


        return render(request,"usuarios/cadastro.html", {"form": form})

def enviar_email(nome, email_cadastro, senha_aleatoria):
    msg = EmailMessage()
    msg['Subject'] = 'Senha de cadastro - Projeto Django'
    msg['From'] = os.getenv('EMAIL')
    msg['To'] = email_cadastro
    msg.set_content(f'Olá {nome}, sua conta foi cadastro foi realizado com sucesso. Sua senha é [{senha_aleatoria}]')

    try:
        with smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525) as smtp:
            smtp.starttls()
            smtp.login(os.getenv('EMAIL'), os.getenv('EMAIL_PASSWORD'))
            smtp.send_message(msg)
         
        print(f'Email enviado com sucesso para [{email_cadastro}]')
    except Exception as e:
        print(f'Erro ao enviar o email: {e}')



