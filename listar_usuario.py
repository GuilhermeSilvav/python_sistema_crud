import tkinter as tk
from tkinter import messagebox
import psycopg2

# Conexão com o banco
def conectar():
    try:
        conn = psycopg2.connect(
            dbname="meu_banco",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar: {e}")
        return None

# Função para listar todos os usuários do banco
def obter_usuarios():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT nome, email FROM usuarios ORDER BY nome")
            usuarios = cur.fetchall()
            cur.close()
            conn.close()
            return usuarios  # lista de tuplas
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuários: {e}")
            return []
    else:
        return []

# Janela para mostrar os usuários
def abrir_listar():
    janela = tk.Toplevel()
    janela.title("Lista de Usuários")
    janela.geometry("500x300")

    tk.Label(janela, text="Usuários cadastrados:", font=("Arial", 12)).pack(pady=10)

    usuarios = obter_usuarios()

    if not usuarios:
        tk.Label(janela, text="Nenhum usuário encontrado.").pack(pady=10)
        return

    # Criar uma área de texto para mostrar os usuários
    texto = tk.Text(janela, width=60, height=15)
    texto.pack(padx=10, pady=10)

    for nome, email in usuarios:
        texto.insert(tk.END, f"Nome: {nome} | Email: {email}\n")

    texto.config(state=tk.DISABLED)  # Impede edição
