import tkinter as tk
from tkinter import messagebox, ttk, filedialog, scrolledtext
import os
import csv
from collections import defaultdict
from datetime import datetime

DB_FILE = "dados.txt"

class AppGerenciador:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Ponto - Filtro por Período (AFD v671)")
        self.root.geometry("800x750")

        self.nome_var = tk.StringVar()
        self.cpf_var = tk.StringVar()
        # Variáveis para o filtro de data
        self.data_inicio_var = tk.StringVar(value="01/01/2026")
        self.data_fim_var = tk.StringVar(value="31/01/2026")
        
        self.editando_cpf_original = None 

        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        # --- FRAME DE CADASTRO ---
        frame_input = tk.LabelFrame(self.root, text=" 1. Cadastro de Funcionários ", padx=10, pady=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Nome:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_input, textvariable=self.nome_var, width=50).grid(row=0, column=1, pady=5)

        tk.Label(frame_input, text="CPF (11 dígitos):").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_input, textvariable=self.cpf_var, width=50).grid(row=1, column=1, pady=5)

        self.btn_salvar = tk.Button(frame_input, text="Salvar Funcionário", command=self.salvar_dados, bg="#4CAF50", fg="white")
        self.btn_salvar.grid(row=2, columnspan=2, pady=10)

        # --- FRAME DE LISTAGEM ---
        frame_lista = tk.LabelFrame(self.root, text=" Funcionários Cadastrados ", padx=10, pady=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_lista, columns=("Nome", "CPF"), show="headings", height=5)
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.pack(fill="both", expand=True)

        btn_edit_frame = tk.Frame(frame_lista)
        btn_edit_frame.pack(pady=5)
        tk.Button(btn_edit_frame, text="Editar", command=self.preparar_edicao, width=10).pack(side="left", padx=5)
        tk.Button(btn_edit_frame, text="Excluir", command=self.excluir_pessoa, bg="#f44336", fg="white", width=10).pack(side="left", padx=5)

        # --- FRAME DE FILTRO E PROCESSAMENTO ---
        frame_afd = tk.LabelFrame(self.root, text=" 2. Processamento AFD com Filtro de Data ", padx=10, pady=10, fg="blue")
        frame_afd.pack(fill="x", padx=10, pady=10)

        # Sub-frame para datas
        date_frame = tk.Frame(frame_afd)
        date_frame.pack(fill="x", pady=5)
        
        tk.Label(date_frame, text="Data Início (DD/MM/AAAA):").pack(side="left")
        tk.Entry(date_frame, textvariable=self.data_inicio_var, width=12).pack(side="left", padx=5)
        
        tk.Label(date_frame, text="Data Fim (DD/MM/AAAA):").pack(side="left", padx=10)
        tk.Entry(date_frame, textvariable=self.data_fim_var, width=12).pack(side="left", padx=5)

        # Botões de ação
        btn_frame = tk.Frame(frame_afd)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="Visualizar Arquivo", command=self.abrir_visualizador_afd, bg="#607D8B", fg="white", width=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="GERAR CSV FILTRADO", command=self.processar_arquivo_relogio, bg="#2196F3", fg="white", width=25).pack(side="right", padx=5)

    # --- FUNÇÕES DE BANCO DE DADOS (TXT) ---
    def salvar_dados(self):
        nome, cpf = self.nome_var.get().strip(), self.cpf_var.get().strip()
        if not nome or len(cpf) != 11:
            messagebox.showwarning("Erro", "CPF deve ter 11 dígitos.")
            return
        linhas = self.ler_arquivo()
        if self.editando_cpf_original:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                for l in linhas:
                    if f";{self.editando_cpf_original}" in l.strip(): f.write(f"{nome};{cpf}\n")
                    else: f.write(l)
            self.editando_cpf_original = None
            self.btn_salvar.config(text="Salvar Funcionário", bg="#4CAF50")
        else:
            with open(DB_FILE, "a", encoding="utf-8") as f: f.write(f"{nome};{cpf}\n")
        self.limpar_campos(); self.carregar_dados()

    def carregar_dados(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for l in self.ler_arquivo():
            if ";" in l: self.tree.insert("", "end", values=l.strip().split(";"))

    def ler_arquivo(self):
        if not os.path.exists(DB_FILE): return []
        with open(DB_FILE, "r", encoding="utf-8") as f: return f.readlines()

    def preparar_edicao(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)['values']
        self.nome_var.set(item[0]); self.cpf_var.set(str(item[1]).zfill(11))
        self.editando_cpf_original = str(item[1]).zfill(11)
        self.btn_salvar.config(text="Confirmar Alteração", bg="#FF9800")

    def excluir_pessoa(self):
        sel = self.tree.selection()
        if not sel: return
        cpf = str(self.tree.item(sel)['values'][1]).zfill(11)
        if messagebox.askyesno("Confirmar", f"Excluir CPF {cpf}?"):
            linhas = [l for l in self.ler_arquivo() if f";{cpf}" not in l.strip()]
            with open(DB_FILE, "w", encoding="utf-8") as f: f.writelines(linhas)
            self.carregar_dados()

    def limpar_campos(self):
        self.nome_var.set(""); self.cpf_var.set("")

    def abrir_visualizador_afd(self):
        caminho = filedialog.askopenfilename()
        if not caminho: return
        try:
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
            janela = tk.Toplevel(self.root)
            janela.title("Visualizador")
            txt = scrolledtext.ScrolledText(janela, wrap=tk.NONE)
            txt.insert(tk.INSERT, conteudo)
            txt.pack(fill="both", expand=True)
        except Exception as e: messagebox.showerror("Erro", str(e))

    # --- LÓGICA DE PROCESSAMENTO COM FILTRO ---
    def processar_arquivo_relogio(self):
        import re  # Certifique-se de que o re está importado
        
        try:
            f_inicio = datetime.strptime(self.data_inicio_var.get(), "%d/%m/%Y")
            f_fim = datetime.strptime(self.data_fim_var.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data de filtro inválido! Use DD/MM/AAAA")
            return

        caminho_afd = filedialog.askopenfilename(title="Selecione o AFD")
        if not caminho_afd: return

        mapa_nomes = {c.zfill(11): n for l in self.ler_arquivo() if ";" in l for n, c in [l.strip().split(";")]}
        batidas = defaultdict(lambda: defaultdict(list))
        
        # Expressão Regular para Registro Tipo 3
        # Grupo 1: Data/Hora variável (YYYY-MM-DDThh:mm:ss[+-]ZZZZ)
        # Grupo 2: CPF exatamente com 12 dígitos
        padrao_tipo3 = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{1,2}:\d{1,2}:\d{1,2}[+-]\d{4})(\d{12})")

        try:
            with open(caminho_afd, "r", encoding="utf-8", errors="ignore") as f:
                for linha in f:
                    linha = linha.strip()
                    if len(linha) > 10 and linha[9] == "3":
                        match = padrao_tipo3.search(linha)
                        if match:
                            dh_completo = match.group(1)
                            cpf_12 = match.group(2)
                            
                            # Extração da Data para o Filtro
                            data_iso = dh_completo[:10]
                            try:
                                data_dt = datetime.strptime(data_iso, "%Y-%m-%d")
                            except: continue

                            if f_inicio <= data_dt <= f_fim:
                                data_br = data_dt.strftime("%d/%m/%Y")
                                
                                # Extração e formatação da Hora (Garante hh:mm:ss)
                                # Pega o trecho entre o 'T' e o fuso (+ ou -)
                                time_match = re.search(r"T(.*?)(?=[+-])", dh_completo)
                                if time_match:
                                    hora_bruta = time_match.group(1)
                                    hora_fmt = ":".join([p.zfill(2) for p in hora_bruta.split(":")])
                                    
                                    # O CPF no AFD tem 12 dígitos (geralmente PIS ou 0+CPF)
                                    # Extraímos os últimos 11 dígitos para bater com o cadastro
                                    cpf_limpo = cpf_12[-11:]
                                    
                                    batidas[cpf_limpo][data_br].append(hora_fmt)
                            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar: {e}"); return

        if not batidas:
            messagebox.showwarning("Aviso", "Nenhum registro encontrado para este período.")
            return

        caminho_csv = filedialog.asksaveasfilename(defaultextension=".csv")
        if not caminho_csv: return

        with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_ALL)
            writer.writerow(["NOME", "CPF", "DATA E HORARIO DE ENTRADA", "DATA E HORARIO DE SAIDA"])

            for cpf, datas in batidas.items():
                nome = mapa_nomes.get(cpf, "NÃO CADASTRADO")
                for data, horarios in datas.items():
                    horarios.sort()
                    ent = f"{data} {horarios[0]}"
                    sai = f"{data} {horarios[-1]}" if len(horarios) > 1 else ""
                    writer.writerow([nome, cpf, ent, sai])

        messagebox.showinfo("Sucesso", f"Relatório de {self.data_inicio_var.get()} a {self.data_fim_var.get()} gerado!")

if __name__ == "__main__":
    root = tk.Tk()
    AppGerenciador(root)
    root.mainloop()
