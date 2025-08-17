import tkinter as tk
from tkinter import messagebox
import psycopg2

# Função para conectar ao banco
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

# Função para buscar usuário pelo nome
def buscar_usuario(nome):
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT nome, email FROM usuarios WHERE nome = %s", (nome,))
            resultado = cur.fetchone()
            cur.close()
            conn.close()
            return resultado  # tupla (nome, email) ou None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")
            return None
    else:
        return None

# Função para atualizar usuário no banco
def atualizar_usuario(nome_antigo, entry_nome, entry_email, janela):
    novo_nome = entry_nome.get()
    novo_email = entry_email.get()

    if not novo_nome or not novo_email:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "UPDATE usuarios SET nome = %s, email = %s WHERE nome = %s"
            cur.execute(sql, (novo_nome, novo_email, nome_antigo))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

# Função para abrir a janela de atualização (recebe dados do usuário)
def abrir_janela_atualizar_com_dados(dados_usuario):
    if dados_usuario is None:
        messagebox.showinfo("Info", "Usuário não encontrado.")
        return

    janela = tk.Toplevel()
    janela.title("Atualizar Usuário")
    janela.geometry("400x250")

    tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.grid(row=0, column=1, padx=10, pady=10)
    entry_nome.insert(0, dados_usuario[0])  # nome

    tk.Label(janela, text="Email:").grid(row=1, column=0, padx=10, pady=10)
    entry_email = tk.Entry(janela, width=40)
    entry_email.grid(row=1, column=1, padx=10, pady=10)
    entry_email.insert(0, dados_usuario[1])  # email

    btn_atualizar = tk.Button(
        janela, text="Atualizar",
        command=lambda: atualizar_usuario(dados_usuario[0], entry_nome, entry_email, janela)
    )
    btn_atualizar.grid(row=2, column=0, columnspan=2, pady=20)

# Função para abrir janela inicial que pede o nome do usuário a ser atualizado
def abrir_atualizar():
    janela = tk.Toplevel()
    janela.title("Buscar Usuário para Atualizar")
    janela.geometry("400x150")

    tk.Label(janela, text="Digite o nome do usuário:").pack(pady=10)
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(pady=5)

    def buscar_e_abrir():
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Atenção", "Digite um nome.")
            return
        dados = buscar_usuario(nome)
        if dados:
            janela.destroy()
            abrir_janela_atualizar_com_dados(dados)
        else:
            messagebox.showinfo("Info", "Usuário não encontrado. Tente novamente.")

    btn_buscar = tk.Button(janela, text="Buscar", command=buscar_e_abrir)
    btn_buscar.pack(pady=10)
