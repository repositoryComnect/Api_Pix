import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests
import base64
import json
import pyperclip
import os
import sys

# Função para obter o caminho da pasta onde o executável está
def recurso_caminho(caminho_relativo):
    try:
        base_path = sys._MEIPASS  # A pasta temporária onde o PyInstaller extrai os arquivos
    except AttributeError:
        base_path = os.path.abspath(".")  # Se estiver rodando pelo script

    return os.path.join(base_path, caminho_relativo)




# Função para carregar credenciais
def carregar_credenciais(caminho_arquivo):
    caminho_completo = recurso_caminho(caminho_arquivo)
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as file:
            credenciais = json.load(file)
        return credenciais
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo de credenciais não encontrado!\n{caminho_completo}")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Erro ao ler o arquivo de credenciais!")
        return None
    



# Função para autenticar e obter o token
def obter_token():
    credenciais = carregar_credenciais('config.json')
    if not credenciais:
        return
    
    client_id = credenciais['client_id']
    client_secret = credenciais['client_secret']
    certificate = credenciais['certificate']
    
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    url = "https://pix-h.api.efipay.com.br/oauth/token"
    
    payload = '{"grant_type": "client_credentials"}'
    headers = {
        'Authorization': f"Basic {auth}",
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, cert=certificate)
        if response.status_code == 200:
            response_data = response.json()
            token = response_data.get('access_token')
            if token:
                token_textbox.delete(1.0, tk.END)
                token_textbox.insert(tk.END, token)
            else:
                messagebox.showerror("Erro", "Token não encontrado na resposta da API!")
        else:
            messagebox.showerror("Erro", f"Erro ao obter token: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer a requisição: {str(e)}")

    root.after(300000, obter_token)




# Função para copiar o token para a área de transferência
def copiar_token():
    token = token_textbox.get(1.0, tk.END).strip()
    if token:
        pyperclip.copy(token)
        messagebox.showinfo("Sucesso", "Token copiado para a área de transferência!")
    else:
        messagebox.showwarning("Aviso", "Nenhum token para copiar!")



        

# Função para criar a interface gráfica
def criar_interface():
    global token_textbox, root, logo_label
    
    root = tk.Tk()
    root.title("Obter Token API")
    root.geometry("600x400")
    root.config(bg="#f0f0f0")

    fonte_moderno = ("Helvetica", 12)

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    # Carregar e exibir o logo
    caminho_logo = recurso_caminho("logo.png")
    if os.path.exists(caminho_logo):
        try:
            logo_img = tk.PhotoImage(file=caminho_logo)
            logo_label = tk.Label(frame, image=logo_img, bg="#f0f0f0")
            logo_label.image = logo_img  # Impede que a imagem seja coletada pelo garbage collector
            logo_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar a imagem: {str(e)}")
    else:
        messagebox.showwarning("Aviso", "Arquivo 'logo.png' não encontrado!")


    obter_token_btn = tk.Button(frame, text="Obter Token", font=fonte_moderno, command=obter_token)
    obter_token_btn.pack(pady=10)

    token_textbox = tk.Text(frame, height=5, width=50, wrap="word", font=fonte_moderno)
    token_textbox.pack(pady=10)

    copiar_token_btn = tk.Button(frame, text="Copiar Token", font=fonte_moderno, command=copiar_token)
    copiar_token_btn.pack(pady=10)

    root.after(5000, obter_token)

    root.mainloop()

criar_interface()
