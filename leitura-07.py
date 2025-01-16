import tkinter as tk
from tkinter import messagebox
import threading
import time


class LeituraRapidaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitura Rápida")
        self.root.geometry("700x500")
        self.root.configure(bg="#faedc9")  # Fundo na cor #faedc9

        # Variáveis
        self.velocidade = tk.IntVar(value=300)  # Velocidade padrão: 300 palavras por minuto
        self.tamanho_fonte = tk.IntVar(value=40)  # Fonte inicial grande

        # Interface principal
        self.create_widgets()

    def create_widgets(self):
        # Título
        tk.Label(self.root, text="Leitura Rápida", bg="#faedc9", font=("Helvetica", 24, "bold")).pack(pady=10)

        # Frame para entrada do texto
        frame_texto = tk.Frame(self.root, bg="#faedc9")
        frame_texto.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(frame_texto, text="Insira o texto:", bg="#faedc9", font=("Helvetica", 12)).pack(anchor="w", padx=5)
        self.text_area = tk.Text(frame_texto, font=("Helvetica", 14), height=8, wrap="word", relief="solid", borderwidth=1)
        self.text_area.pack(padx=5, pady=5, fill="both", expand=True)

        # Frame para configurações
        frame_config = tk.Frame(self.root, bg="#faedc9")
        frame_config.pack(pady=10, fill="x")

        tk.Label(frame_config, text="Velocidade (palavras por minuto):", bg="#faedc9", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.speed_entry = tk.Entry(frame_config, textvariable=self.velocidade, font=("Helvetica", 14), width=8)
        self.speed_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(frame_config, text="Tamanho da fonte:", bg="#faedc9", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.font_size_entry = tk.Entry(frame_config, textvariable=self.tamanho_fonte, font=("Helvetica", 14), width=8)
        self.font_size_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Botões
        frame_botoes = tk.Frame(self.root, bg="#faedc9")
        frame_botoes.pack(pady=10)

        self.calculate_button = tk.Button(
            frame_botoes, text="Calcular Estimativa", command=self.calcular_estimativa,
            bg="#007BFF", fg="black", font=("Helvetica", 14), relief="flat", activebackground="#0056b3", activeforeground="white"
        )
        self.calculate_button.grid(row=0, column=0, padx=10)

        self.start_button = tk.Button(
            frame_botoes, text="Iniciar Leitura", command=self.iniciar_leitura,
            bg="#007BFF", fg="black", font=("Helvetica", 14), relief="flat", activebackground="#0056b3", activeforeground="white"
        )
        self.start_button.grid(row=0, column=1, padx=10)

        # Área para exibir estimativa
        frame_estimativa = tk.Frame(self.root, bg="#faedc9", relief="solid", borderwidth=1)
        frame_estimativa.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_estimativa, text="Estimativa de Tempo:", bg="#faedc9", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        self.estimate_label = tk.Label(frame_estimativa, text="", bg="#faedc9", font=("Helvetica", 12), justify="left")
        self.estimate_label.pack(anchor="w", padx=10, pady=5)

    def calcular_estimativa(self):
        texto = self.text_area.get("1.0", tk.END).strip()
        palavras = len(texto.split())
        velocidade_usuario = self.velocidade.get()

        if not texto:
            messagebox.showerror("Erro", "Por favor, insira um texto.")
            return

        if palavras == 0:
            self.estimate_label.config(text="O texto está vazio.")
            return

        # Velocidade média humana
        velocidade_media = 225  # palavras por minuto
        tempo_medio = palavras / velocidade_media  # tempo em minutos
        tempo_usuario = palavras / velocidade_usuario if velocidade_usuario > 0 else 0  # tempo com velocidade definida

        # Atualiza o texto da estimativa
        estimativa_texto = (
            f"Texto contém {palavras} palavras.\n"
            f"Tempo estimado na velocidade média humana (225 WPM): {tempo_medio:.2f} minutos.\n"
            f"Tempo estimado na sua velocidade ({velocidade_usuario} WPM): {tempo_usuario:.2f} minutos."
        )
        self.estimate_label.config(text=estimativa_texto)

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

        # Legenda dinâmica para mostrar a velocidade atual
        self.legend = tk.Label(
            leitura_window,
            text=f"Atalhos: ESC - Sair | + - Aumentar Velocidade | - - Reduzir Velocidade | Velocidade: {velocidade} WPM",
            bg="#faedc9",
            font=("Helvetica", 10),
        )
        self.legend.pack(side="bottom", pady=5)

        # Variáveis para controle
        self.texto_palavras = texto.split()
        self.velocidade_atual = velocidade
        self.palavra_atual = 0
        self.pausado = False  # Variável de pausa

        # Bind das teclas de atalho
        leitura_window.bind("<Escape>", lambda e: leitura_window.destroy())
        leitura_window.bind("<plus>", lambda e: self.ajustar_velocidade(10))
        leitura_window.bind("<minus>", lambda e: self.ajustar_velocidade(-10))
        leitura_window.bind("<space>", lambda e: self.toggle_pausa())

        # Inicia a leitura em uma thread separada
        threading.Thread(target=self.exibir_palavras, args=(display_label, leitura_window), daemon=True).start()

    def ajustar_velocidade(self, ajuste):
        self.velocidade_atual += ajuste
        if self.velocidade_atual < 10:  # Limita velocidade mínima
            self.velocidade_atual = 10
        self.legend.config(
            text=f"Atalhos: ESC - Sair | + - Aumentar Velocidade | - - Reduzir Velocidade | Velocidade: {self.velocidade_atual} WPM"
        )

    def toggle_pausa(self):
        self.pausado = not self.pausado

    def exibir_palavras(self, display_label, leitura_window):
        while self.palavra_atual < len(self.texto_palavras):
            while self.pausado:  # Verifica se está pausado
                time.sleep(0.1)  # Aguarda até sair do modo pausado
            display_label.config(text=self.texto_palavras[self.palavra_atual])
            time.sleep(60 / self.velocidade_atual)
            self.palavra_atual += 1


# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = LeituraRapidaApp(root)
    root.mainloop()
