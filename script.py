from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

# Configurações do tamanho das cartas (59mm x 86mm)
CARD_WIDTH_MM = 59
CARD_HEIGHT_MM = 86
MM_TO_POINTS = 2.83465  # 1 mm = 2.83465 pontos no PDF
CARD_WIDTH_PT = CARD_WIDTH_MM * MM_TO_POINTS
CARD_HEIGHT_PT = CARD_HEIGHT_MM * MM_TO_POINTS

# Tamanho da página A4 em pontos
PAGE_WIDTH, PAGE_HEIGHT = A4

# Função para criar o PDF
def create_pdf(image_paths, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Calcula o número de colunas e linhas
    max_columns = 3  # 3 cartas horizontalmente
    max_rows = 3     # 3 cartas verticalmente

    x = 0  # Começa na borda esquerda
    y = PAGE_HEIGHT - CARD_HEIGHT_PT  # Começa no topo

    for idx, img_path in enumerate(image_paths):
        # Abrir a imagem original
        img = Image.open(img_path)

        # Calcula posição centralizada dentro do espaço da carta
        offset_x = (CARD_WIDTH_PT - img.width) / 2
        offset_y = (CARD_HEIGHT_PT - img.height) / 2

        # Adicionar imagem ao PDF a partir do arquivo temporário
        c.drawImage(img_path, x + offset_x+417, y + offset_y+471, width=CARD_WIDTH_PT, height=CARD_HEIGHT_PT)

        # Atualizar posição para a próxima carta
        x += CARD_WIDTH_PT  # Move para a próxima coluna
        if (idx + 1) % max_columns == 0:  # Se for a última coluna
            x = 0  # Volta para a primeira coluna
            y -= CARD_HEIGHT_PT  # Move para a próxima linha
            if y < 0:  # Se ultrapassar o limite inferior da página
                c.showPage()  # Cria uma nova página
                y = PAGE_HEIGHT - CARD_HEIGHT_PT  # Reseta para o topo
                x = 0  # Reseta para a primeira coluna

    c.save()  # Salva o PDF

# Diretório com imagens
image_directory = "imagens"  # Substitua pelo seu diretório
image_files = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Nome do PDF de saída
output_pdf = "cartas_jogo_alta_qualidade.pdf"

create_pdf(image_files, output_pdf)
print(f"PDF gerado com sucesso: {output_pdf}")
