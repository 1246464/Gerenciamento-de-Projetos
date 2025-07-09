from fpdf import FPDF
import datetime
import os
import platform
import csv
import matplotlib.pyplot as plt

# -----------------------
# Utilitários
# -----------------------

def abrir_arquivo(nome_arquivo):
    """Abre um arquivo conforme o sistema operacional."""
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(nome_arquivo)
        elif sistema == "Darwin":  # macOS
            os.system(f"open '{nome_arquivo}'")
        else:  # Linux
            os.system(f"xdg-open '{nome_arquivo}'")
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")

# -----------------------
# Exportar PDF do projeto
# -----------------------

def gerar_pdf_projeto(projeto):
    """Gera um relatório em PDF com os dados do projeto."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    data_geracao = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    nome_proj = projeto.get('nome', 'Projeto Sem Nome')
    pdf.cell(200, 10, txt=f"Relatório do Projeto - {nome_proj}", ln=True, align="C")

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Gerado em: {data_geracao}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=f"Projeto: {nome_proj}", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, txt=f"Descrição: {projeto.get('descricao', 'Sem descrição')}")
    pdf.cell(200, 8, txt=f"ID: {projeto.get('id', 'N/D')}", ln=True)

    etapas = projeto.get("etapas", [])
    pdf.ln(4)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(200, 8, txt="Etapas:", ln=True)
    pdf.set_font("Arial", "", 10)

    if etapas:
        for etapa in etapas:
            texto = (
                f"- {etapa.get('nome', '-')}, "
                f"Status: {etapa.get('status', '-')}, "
                f"Prazo: {etapa.get('prazo', '-')}, "
                f"Responsável: {etapa.get('responsavel', '-')}"
            )
            pdf.multi_cell(0, 8, txt=texto)
    else:
        pdf.cell(200, 8, txt="Sem etapas cadastradas", ln=True)

    nome_arquivo = f"relatorio_projeto_{projeto.get('id', 'sem_id')}.pdf"
    pdf.output(nome_arquivo)
    abrir_arquivo(nome_arquivo)

# -----------------------
# Gráfico de Barras Horizontais
# -----------------------

def gerar_grafico_barras(projeto):
    """Gera um gráfico horizontal de barras com o status das etapas."""
    etapas = projeto.get("etapas", [])
    if not etapas:
        print("Sem etapas para gerar gráfico.")
        return

    nomes = [etapa.get("nome", "-") for etapa in etapas]
    status = [etapa.get("status", "-") for etapa in etapas]

    cores = {
        "pendente": "gray",
        "em andamento": "orange",
        "concluído": "green"
    }
    cor_barras = [cores.get(s, "blue") for s in status]

    fig, ax = plt.subplots(figsize=(10, len(nomes) * 0.5))
    ax.barh(nomes, [1] * len(nomes), color=cor_barras)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title(f"Etapas do Projeto: {projeto.get('nome', '-')}")
    for i, s in enumerate(status):
        ax.text(0.5, i, s, ha='center', va='center', color='white', fontsize=10)

    plt.tight_layout()
    nome_arquivo = f"grafico_projeto_{projeto.get('id')}.png"
    plt.savefig(nome_arquivo)
    abrir_arquivo(nome_arquivo)

# -----------------------
# Exportar CSV do projeto
# -----------------------

def exportar_csv_projeto(projeto):
    """Exporta as etapas do projeto em formato CSV."""
    nome_arquivo = f"projeto_{projeto.get('id')}.csv"
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Etapa", "Status", "Prazo", "Responsável"])
        for etapa in projeto.get("etapas", []):
            writer.writerow([
                etapa.get("nome", ""),
                etapa.get("status", ""),
                etapa.get("prazo", ""),
                etapa.get("responsavel", "")
            ])
    abrir_arquivo(nome_arquivo)
