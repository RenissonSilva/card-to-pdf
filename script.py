from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os
import io
import tempfile  # Para criar arquivos temporários

# Configurações do tamanho das cartas (59mm x 86mm)
CARD_WIDTH_MM = 59
CARD_HEIGHT_MM = 86
MM_TO_POINTS = 2.83465  # 1 mm = 2.83465 pontos no PDF
CARD_WIDTH_PT = CARD_WIDTH_MM * MM_TO_POINTS
CARD_HEIGHT_PT = CARD_HEIGHT_MM * MM_TO_POINTS

# Tamanho da página A4 em pontos
PAGE_WIDTH, PAGE_HEIGHT = A4

# Função para redimensionar a imagem mantendo a proporção
def resize_image_keep_aspect(img, target_width, target_height):
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    if (target_width / target_height) > aspect_ratio:
        # Ajusta pela altura
        new_height = int(target_height)
        new_width = int(aspect_ratio * target_height)
    else:
        # Ajusta pela largura
        new_width = int(target_width)
        new_height = int(target_width / aspect_ratio)

    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Função para criar o PDF
def create_pdf(image_paths, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Calcula o número de colunas e linhas
    max_columns = 3  # 3 cartas horizontalmente
    max_rows = 3     # 3 cartas verticalmente

    x = 0  # Começa na borda esquerda
    y = PAGE_HEIGHT - CARD_HEIGHT_PT  # Começa no topo

    for idx, img_path in enumerate(image_paths):
        # Abrir a imagem e redimensionar mantendo proporção
        img = Image.open(img_path)
        resized_img = resize_image_keep_aspect(img, CARD_WIDTH_PT, CARD_HEIGHT_PT)

        # Converte a imagem redimensionada para o modo RGB, se necessário
        if resized_img.mode != "RGB":
            resized_img = resized_img.convert("RGB")

        # Criar um arquivo temporário para a imagem redimensionada
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            resized_img.save(temp_file, format="PNG")
            temp_file_path = temp_file.name

        # Calcula posição centralizada dentro do espaço da carta
        offset_x = (CARD_WIDTH_PT - resized_img.width) / 2
        offset_y = (CARD_HEIGHT_PT - resized_img.height) / 2

        # Adicionar imagem ao PDF a partir do arquivo temporário
        c.drawImage(temp_file_path, x + offset_x, y + offset_y, width=resized_img.width, height=resized_img.height)

        # Atualizar posição para a próxima carta
        x += CARD_WIDTH_PT  # Move para a próxima coluna
        if (idx + 1) % max_columns == 0:  # Se for a última coluna
            x = 0  # Volta para a primeira coluna
            y -= CARD_HEIGHT_PT  # Move para a próxima linha
            if y < 0:  # Se ultrapassar o limite inferior da página
                c.showPage()  # Cria uma nova página
                y = PAGE_HEIGHT - CARD_HEIGHT_PT  # Reseta para o topo
                x = 0  # Reseta para a primeira coluna

        # Remover o arquivo temporário após o uso
        os.remove(temp_file_path)

    c.save()  # Salva o PDF

# Diretório com imagens
image_directory = "imagens"  # Substitua pelo seu diretório
image_files = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Nome do PDF de saída
output_pdf = "cartas_jogo_alta_qualidade.pdf"

create_pdf(image_files, output_pdf)
print(f"PDF gerado com sucesso: {output_pdf}")
