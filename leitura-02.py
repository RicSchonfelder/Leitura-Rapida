import tkinter as tk
from tkinter import messagebox
import time
import threading

class LeituraRapidaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitura Rápida")
        self.root.geometry("800x400")
        self.root.configure(bg="#FFA07A")  # Fundo cor salmão

        # Variáveis
        self.texto = tk.StringVar()
        self.velocidade = tk.IntVar(value=300)  # Padrão: 300 palavras por minuto
        self.tamanho_fonte = tk.IntVar(value=40)  # Fonte inicial grande

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Entrada do texto
        tk.Label(self.root, text="Insira o texto:", bg="#FFA07A", font=("Helvetica", 12)).pack(pady=5)
        self.text_entry = tk.Entry(self.root, textvariable=self.texto, font=("Helvetica", 14), width=80)
        self.text_entry.pack(pady=5)

        # Configuração da velocidade
        tk.Label(self.root, text="Velocidade (palavras por minuto):", bg="#FFA07A", font=("Helvetica", 12)).pack(pady=5)
        self.speed_entry = tk.Entry(self.root, textvariable=self.velocidade, font=("Helvetica", 14), width=10)
        self.speed_entry.pack(pady=5)

        # Configuração do tamanho da fonte
        tk.Label(self.root, text="Tamanho da fonte:", bg="#FFA07A", font=("Helvetica", 12)).pack(pady=5)
        self.font_size_entry = tk.Entry(self.root, textvariable=self.tamanho_fonte, font=("Helvetica", 14), width=10)
        self.font_size_entry.pack(pady=5)

        # Botão de iniciar leitura
        self.start_button = tk.Button(self.root, text="Iniciar Leitura", command=self.iniciar_leitura, bg="#FF6347", fg="white", font=("Helvetica", 14))
        self.start_button.pack(pady=10)

        # Área de exibição
        self.display_label = tk.Label(self.root, text="", bg="#FFA07A", font=("Helvetica", self.tamanho_fonte.get()), wraplength=700)
        self.display_label.pack(expand=True)

    def iniciar_leitura(self):
        texto = self.texto.get()
        velocidade = self.velocidade.get()
        tamanho_fonte = self.tamanho_fonte.get()

        if not texto.strip():
            messagebox.showerror("Erro", "Por favor, insira um texto.")
            return

        if velocidade <= 0:
            messagebox.showerror("Erro", "A velocidade deve ser maior que 0.")
            return

        if tamanho_fonte <= 0:
            messagebox.showerror("Erro", "O tamanho da fonte deve ser maior que 0.")
            return

        # Atualiza o tamanho da fonte
        self.display_label.config(font=("Helvetica", tamanho_fonte))

        # Inicia a leitura em uma thread separada
        threading.Thread(target=self.exibir_palavras, args=(texto, velocidade), daemon=True).start()

    def exibir_palavras(self, texto, velocidade):
        palavras = texto.split()
        intervalo = 60 / velocidade

        for palavra in palavras:
            self.display_label.config(text=palavra)
            time.sleep(intervalo)

        # Finaliza a leitura
        self.display_label.config(text="Leitura concluída!")

# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = LeituraRapidaApp(root)
    root.mainloop()
