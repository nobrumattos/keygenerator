import secrets
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from cryptography.fernet import Fernet
import time
import threading

# Definindo conjuntos de caracteres
CARACTERES = {
    'hex': '0123456789abcdef',
    'bin': '01',
    'base64': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',
    'especial': '!"#$%&\'()*+,-./:;<=>?@[\\]_^`{|}~'
}

class GeradorDeSenhas:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Gerador de Senhas Ultra Complexas")
        self.janela.geometry("600x700")  # Ajustado para mais espaço
        self.janela.configure(bg='#f0f0f0')

        self.configurar_widgets()

    def gerar_chave(self):
        return Fernet.generate_key()

    def criar_fernet(self, chave):
        return Fernet(chave)

    def gerar_senha(self, tamanho, tipo='hex'):
        if tipo not in CARACTERES:
            raise ValueError("Tipo de senha não suportado.")
        caracteres = CARACTERES[tipo]
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        return senha

    def validar_senha(self, senha, tipo):
        padroes = {
            'hex': r'^[0-9a-fA-F]{16,}$',
            'bin': r'^[01]{16,}$',
            'base64': r'^[A-Za-z0-9+/=]{16,}$',
            'especial': r'^[ !"#$%&\'()*+,-./:;<=>?@[\\]_^`{|}~]{16,}$'
        }
        if tipo not in padroes:
            raise ValueError("Tipo de senha não suportado.")
        padrao = padroes[tipo]
        match = re.fullmatch(padrao, senha)
        return match is not None

    def criptografar_senha(self, fernet, senha):
        return fernet.encrypt(senha.encode()).decode()

    def descriptografar_senha(self, fernet, senha_criptografada):
        return fernet.decrypt(senha_criptografada.encode()).decode()

    def atualizar_progresso(self, descricao, progresso, tempo_restante):
        self.label_progresso.config(text=f"{descricao}\n{progresso}\nTempo restante: {tempo_restante}")
        self.janela.update_idletasks()

    def mostrar_mensagem(self, mensagem):
        self.label_mensagem.config(text=mensagem)
        self.janela.update_idletasks()

    def animar_carregamento(self, callback):
        etapas = [
            ("🔑 Gerando chave de criptografia...", 10),
            ("🔍 Aplicando camadas de proteção...", 20),
            ("💾 Codificando a senha...", 30),
        ]

        def animação():
            tempo_acumulado = 0
            for descricao, progresso_max in etapas:
                for i in range(0, progresso_max + 1, 2):  # Atualiza o progresso a cada 0.5s
                    tempo_restante = f"{(progresso_max - i) * 0.1:.1f}s"
                    progresso = f"{'█' * (i // 2)}{'░' * ((progresso_max - i) // 2)}"
                    self.atualizar_progresso(descricao, progresso, tempo_restante)
                    time.sleep(0.1)
                tempo_acumulado += progresso_max
                time.sleep(1)  # Delay entre etapas

            self.janela.after(0, callback)  # Chama o callback após a animação

        threading.Thread(target=animação, daemon=True).start()

    def gerar_senha_completa(self):
        def gerar_senha_e_mostrar_resultado():
            try:
                tamanho = int(self.entry_tamanho.get() or 16)
                if tamanho < 16:
                    messagebox.showwarning("Aviso", "O comprimento da senha deve ser de pelo menos 16 caracteres para garantir a complexidade.")
                    return

                tipo = self.tipo_senha.get()

                chave = self.gerar_chave()
                fernet = self.criar_fernet(chave)

                senha = self.gerar_senha(tamanho, tipo)
                senha_criptografada = self.criptografar_senha(fernet, senha)
                senha_descriptografada = self.descriptografar_senha(fernet, senha_criptografada)

                if self.validar_senha(senha, tipo):
                    resultado = (f"Sua senha gerada é: {senha}\n"
                                 f"Senha criptografada é: {senha_criptografada}\n"
                                 f"Senha descriptografada é: {senha_descriptografada}\n"
                                 f"\nChave de criptografia:\n{chave.decode()}")

                    def mostrar_resultado():
                        messagebox.showinfo("Resultado", "Senha gerada com sucesso!")
                        self.text_resultado.config(state=tk.NORMAL)
                        self.text_resultado.delete(1.0, tk.END)
                        self.text_resultado.insert(tk.END, resultado)
                        self.text_resultado.config(state=tk.DISABLED)

                    mostrar_resultado()
                else:
                    messagebox.showerror("Erro", "Erro na geração ou validação da senha.")
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

        self.mostrar_mensagem("Gerando senha...")
        self.animar_carregamento(gerar_senha_e_mostrar_resultado)

    def copiar_para_area_de_transferencia(self):
        self.janela.clipboard_clear()
        self.janela.clipboard_append(self.text_resultado.get(1.0, tk.END).strip())
        messagebox.showinfo("Copiado", "Texto copiado para a área de transferência!")

    def configurar_widgets(self):
        # Frame centralizado para os widgets
        frame = tk.Frame(self.janela, bg='#f0f0f0', padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        # Labels e Entradas
        tk.Label(frame, text="Comprimento da senha:", bg='#f0f0f0', fg='#000000', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_tamanho = tk.Entry(frame, font=('Arial', 12), bg='#ffffff', fg='#000000', bd=1, relief='solid', width=20)
        self.entry_tamanho.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(frame, text="Tipo de senha:", bg='#f0f0f0', fg='#000000', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')

        tipo_frame = tk.Frame(frame, bg='#f0f0f0')
        tipo_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.tipo_senha = tk.StringVar(value='hex')
        for tipo in CARACTERES.keys():
            tk.Radiobutton(tipo_frame, text=tipo, variable=self.tipo_senha, value=tipo, bg='#f0f0f0', fg='#000000', font=('Arial', 10), selectcolor='#d0d0d0', indicatoron=0, bd=1, relief='solid').pack(side=tk.LEFT, padx=5)

        # Botões
        tk.Button(frame, text="Gerar Senha", command=self.gerar_senha_completa, bg='#4CAF50', fg='#ffffff', font=('Arial', 12), relief='raised', bd=1).grid(row=2, column=0, columnspan=2, pady=15, sticky='ew')

        tk.Button(frame, text="Copiar para Área de Transferência", command=self.copiar_para_area_de_transferencia, bg='#2196F3', fg='#ffffff', font=('Arial', 12), relief='raised', bd=1).grid(row=3, column=0, columnspan=2, pady=15, sticky='ew')

        # Progresso
        self.label_progresso = tk.Label(frame, text="", bg='#f0f0f0', fg='#000000', font=('Arial', 12))
        self.label_progresso.grid(row=4, column=0, columnspan=2, pady=15)

        # Mensagens de Carregamento
        self.label_mensagem = tk.Label(frame, text="", bg='#f0f0f0', fg='#000000', font=('Arial', 12))
        self.label_mensagem.grid(row=5, column=0, columnspan=2, pady=10)

        # Resultado
        tk.Label(frame, text="Resultado:", bg='#f0f0f0', fg='#000000', font=('Arial', 12)).grid(row=6, column=0, padx=10, pady=10, sticky='nw')
        self.text_resultado = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, width=70, font=('Arial', 12), bg='#ffffff', fg='#000000', state=tk.DISABLED)
        self.text_resultado.grid(row=6, column=1, padx=10, pady=10)

# Criando a janela principal
root = tk.Tk()
app = GeradorDeSenhas(root)
root.mainloop()
