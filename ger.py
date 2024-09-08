import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import secrets
import logging
from cryptography.fernet import Fernet

# Configuração de logging
logging.basicConfig(filename='erros.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

CARACTERES = {
    'hex': '0123456789abcdef',
    'bin': '01',
    'base64': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
    'especial': ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
}

def capturar_erro():
    logging.error("Erro capturado", exc_info=True)

class GeradorDeSenhas:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Gerador de Senhas")
        self.janela.geometry("600x700")
        self.janela.configure(bg='#f0f0f0')
        self.configurar_widgets()

    def configurar_widgets(self):
        try:
            frame = tk.Frame(self.janela, bg='#f0f0f0', padx=20, pady=20)
            frame.pack(expand=True, fill='both')

            # Labels e Entradas
            tk.Label(frame, text="Comprimento da senha:", bg='#f0f0f0', fg='#000000', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
            self.entry_tamanho = tk.Entry(frame, font=('Arial', 12), bg='#ffffff', fg='#000000', bd=1, relief='solid', width=20)
            self.entry_tamanho.grid(row=0, column=1, padx=10, pady=10, sticky='w')

            tk.Label(frame, text="Tipo de senha:", bg='#f0f0f0', fg='#000000', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
            self.tipo_senha = tk.StringVar(value='hex')
            tk.OptionMenu(frame, self.tipo_senha, *CARACTERES.keys()).grid(row=1, column=1, padx=10, pady=10, sticky='w')

            # Label para progresso
            self.label_progresso = tk.Label(frame, text="", bg='#f0f0f0', fg='#000000', font=('Arial', 12))
            self.label_progresso.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            # Botão de gerar senha
            tk.Button(frame, text="Gerar Senha", command=self.gerar_senha_completa, font=('Arial', 12), bg='#4CAF50', fg='#ffffff').grid(row=3, column=0, columnspan=2, padx=10, pady=10)

            # Campo de resultado
            self.text_resultado = scrolledtext.ScrolledText(frame, height=10, width=70, wrap=tk.WORD, state=tk.DISABLED, bg='#ffffff', fg='#000000', font=('Arial', 12))
            self.text_resultado.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

            # Botão para copiar
            tk.Button(frame, text="Copiar para área de transferência", command=self.copiar_para_area_de_transferencia, font=('Arial', 12), bg='#2196F3', fg='#ffffff').grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            # Label de mensagens
            self.label_mensagem = tk.Label(frame, text="", bg='#f0f0f0', fg='#ff0000', font=('Arial', 12))
            self.label_mensagem.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        except Exception as e:
            capturar_erro()
            messagebox.showerror("Erro", "Ocorreu um erro ao configurar os widgets.")

    def gerar_chave(self):
        try:
            return Fernet.generate_key()
        except Exception as e:
            logging.error(f"Erro ao gerar chave: {e}", exc_info=True)

    def criar_fernet(self, chave):
        try:
            return Fernet(chave)
        except Exception as e:
            logging.error(f"Erro ao criar Fernet: {e}", exc_info=True)

    def gerar_senha(self, tamanho, tipo='hex'):
        try:
            if tipo not in CARACTERES:
                raise ValueError("Tipo de senha não suportado.")
            if not (8 <= tamanho <= 16):
                raise ValueError("O tamanho da senha deve estar entre 8 e 16 caracteres.")
            if tipo == 'especial' and tamanho < 8:
                raise ValueError("Para senhas especiais, o comprimento deve ser pelo menos 8 caracteres.")
            return ''.join(secrets.choice(CARACTERES[tipo]) for _ in range(tamanho))
        except Exception as e:
            logging.error(f"Erro ao gerar senha: {e}", exc_info=True)
            raise

    def criptografar_senha(self, fernet, senha):
        try:
            return fernet.encrypt(senha.encode()).decode()
        except Exception as e:
            logging.error(f"Erro ao criptografar senha: {e}", exc_info=True)

    def descriptografar_senha(self, fernet, senha_criptografada):
        try:
            return fernet.decrypt(senha_criptografada.encode()).decode()
        except Exception as e:
            logging.error(f"Erro ao descriptografar senha: {e}", exc_info=True)

    def atualizar_progresso(self, descricao, progresso, tempo_restante):
        try:
            if hasattr(self, 'label_progresso'):
                self.label_progresso.config(text=f"{descricao}\n{progresso}\nTempo restante: {tempo_restante}")
        except Exception as e:
            logging.error(f"Erro ao atualizar progresso: {e}", exc_info=True)

    def mostrar_mensagem(self, mensagem):
        try:
            if hasattr(self, 'label_mensagem'):
                self.label_mensagem.config(text=mensagem)
        except Exception as e:
            logging.error(f"Erro ao mostrar mensagem: {e}", exc_info=True)

    def animar_carregamento(self, callback):
        etapas = [
            ("🔑 Gerando chave de criptografia...", 10),
            ("🔍 Aplicando camadas de proteção...", 20),
            ("💾 Codificando a senha...", 30),
        ]

        def animacao(index=0, progresso=0):
            try:
                if index < len(etapas):
                    descricao, progresso_max = etapas[index]
                    if progresso <= progresso_max:
                        tempo_restante = f"{(progresso_max - progresso) * 0.05:.1f}s"
                        self.atualizar_progresso(descricao, progresso, tempo_restante)
                        self.janela.after(50, animacao, index, progresso + 1)
                    else:
                        self.janela.after(500, animacao, index + 1)
                else:
                    self.janela.after(0, callback)
            except Exception as e:
                logging.error(f"Erro na animação: {e}", exc_info=True)

        animacao()

    def gerar_senha_completa(self):
        def gerar_senha_e_mostrar_resultado():
            try:
                tamanho = int(self.entry_tamanho.get() or 16)
                
                if tamanho < 8 or tamanho > 16:
                    messagebox.showwarning("Aviso", "O comprimento da senha deve estar entre 8 e 16 caracteres.")
                    return

                tipo = self.tipo_senha.get()

                chave = self.gerar_chave()
                fernet = self.criar_fernet(chave)

                senha = self.gerar_senha(tamanho, tipo)
                senha_criptografada = self.criptografar_senha(fernet, senha)
                senha_descriptografada = self.descriptografar_senha(fernet, senha_criptografada)

                if self.validar_senha(senha_descriptografada, tipo):
                    self.text_resultado.config(state=tk.NORMAL)
                    self.text_resultado.delete(1.0, tk.END)
                    self.text_resultado.insert(tk.END, f"Senha gerada: {senha}\n")
                    self.text_resultado.insert(tk.END, f"Senha criptografada: {senha_criptografada}\n")
                    self.text_resultado.insert(tk.END, f"Senha descriptografada: {senha_descriptografada}\n")
                    self.text_resultado.config(state=tk.DISABLED)
                    self.mostrar_mensagem("Senha gerada com sucesso!")
                else:
                    self.mostrar_mensagem("Senha gerada é inválida. Tente novamente.")
            except Exception as e:
                capturar_erro()
                messagebox.showerror("Erro", "Ocorreu um erro ao gerar a senha.")

        self.animar_carregamento(gerar_senha_e_mostrar_resultado)

    def copiar_para_area_de_transferencia(self):
        try:
            self.janela.clipboard_clear()
            self.janela.clipboard_append(self.text_resultado.get(1.0, tk.END).strip())
            self.janela.update()
            self.mostrar_mensagem("Senha copiada para a área de transferência!")
        except Exception as e:
            logging.error(f"Erro ao copiar para a área de transferência: {e}", exc_info=True)
            messagebox.showerror("Erro", "Ocorreu um erro ao copiar para a área de transferência.")

    def validar_senha(self, senha, tipo):
        try:
            if tipo == 'especial':
                if all(c in CARACTERES[tipo] for c in senha):
                    return True
                else:
                    return False
            else:
                if all(c in CARACTERES[tipo] for c in senha):
                    return True
                else:
                    return False
        except Exception as e:
            logging.error(f"Erro ao validar senha: {e}", exc_info=True)
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorDeSenhas(root)
    root.mainloop()
