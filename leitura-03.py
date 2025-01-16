import tkinter as tk
from tkinter import messagebox
import threading
import time


class LeituraRapidaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitura Rápida")
        self.root.geometry("600x400")
        self.root.configure(bg="#faedc9")  # Fundo na cor #faedc9

        # Variáveis
        self.velocidade = tk.IntVar(value=300)  # Velocidade padrão: 300 palavras por minuto
        self.tamanho_fonte = tk.IntVar(value=40)  # Fonte inicial grande

        # Interface principal
        self.create_widgets()

    def create_widgets(self):
        # Título
        tk.Label(self.root, text="Leitura Rápida", bg="#faedc9", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Área de texto
        tk.Label(self.root, text="Insira o texto:", bg="#faedc9", font=("Helvetica", 12)).pack(anchor="w", padx=10)
        self.text_area = tk.Text(self.root, font=("Helvetica", 14), height=8, wrap="word")
        self.text_area.pack(padx=10, pady=5, fill="both", expand=True)

        # Configuração da velocidade
        tk.Label(self.root, text="Velocidade (palavras por minuto):", bg="#faedc9", font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=5)
        self.speed_entry = tk.Entry(self.root, textvariable=self.velocidade, font=("Helvetica", 14), width=10)
        self.speed_entry.pack(anchor="w", padx=10)

        # Configuração do tamanho da fonte
        tk.Label(self.root, text="Tamanho da fonte:", bg="#faedc9", font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=5)
        self.font_size_entry = tk.Entry(self.root, textvariable=self.tamanho_fonte, font=("Helvetica", 14), width=10)
        self.font_size_entry.pack(anchor="w", padx=10)

        # Botão para iniciar leitura
        self.start_button = tk.Button(self.root, text="Iniciar Leitura", command=self.iniciar_leitura, bg="#86c8bc", fg="white", font=("Helvetica", 14))
        self.start_button.pack(pady=15)

    def iniciar_leitura(self):
        texto = self.text_area.get("1.0", tk.END).strip()
        velocidade = self.velocidade.get()
        tamanho_fonte = self.tamanho_fonte.get()

        if not texto:
            messagebox.showerror("Erro", "Por favor, insira um texto.")
            return

        if velocidade <= 0:
            messagebox.showerror("Erro", "A velocidade deve ser maior que 0.")
            return

        if tamanho_fonte <= 0:
            messagebox.showerror("Erro", "O tamanho da fonte deve ser maior que 0.")
            return

        # Cria uma nova janela para exibir as palavras
        leitura_window = tk.Toplevel(self.root)
        leitura_window.title("Exibição de Leitura")
        leitura_window.geometry("800x400")
        leitura_window.configure(bg="#faedc9")

        display_label = tk.Label(
            leitura_window, text="", bg="#faedc9", font=("Helvetica", tamanho_fonte), wraplength=700
        )
        display_label.pack(expand=True)

        # Inicia a leitura em uma thread separada
        threading.Thread(target=self.exibir_palavras, args=(texto, velocidade, display_label), daemon=True).start()

    def exibir_palavras(self, texto, velocidade, display_label):
        palavras = texto.split()
        intervalo = 60 / velocidade

        for palavra in palavras:
            display_label.config(text=palavra)
            time.sleep(intervalo)

        # Finaliza a leitura
        display_label.config(text="Leitura concluída!")


# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = LeituraRapidaApp(root)
    root.mainloop()
