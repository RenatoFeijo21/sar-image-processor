import numpy as np
import rasterio
import os

def cfar_process(image_path, k=3.29, win=2):
    """
    Processa a imagem SAR com CFAR 5x5 (99.5%) e salva com sufixo 'CFARproc'.
    
    Args:
        image_path (str): Caminho da imagem SAR.
        k (float): Fator de threshold (default 3.29 ~ 99.5% confiança).
        win (int): Meio tamanho da janela (win=2 gera 5x5).
    
    Returns:
        output (np.array): Imagem binária processada.
    """

    with rasterio.open(image_path) as src:
        image = src.read(1)
        meta = src.meta

    rows, cols = image.shape
    output = np.zeros_like(image, dtype=np.uint8)

    for i in range(win, rows - win):
        for j in range(win, cols - win):
            window = image[i-win:i+win+1, j-win:j+win+1].flatten()
            guard = image[i,j]
            mean = np.mean(window)
            std = np.std(window)
            threshold = mean + k * std

            output[i,j] = 255 if guard > threshold else 0

    # Salvando imagem processada com novo nome
    dir_name = os.path.dirname(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    new_name = f"{name}_CFARproc{ext}"
    new_path = os.path.join(dir_name, new_name)

    meta.update(dtype=rasterio.uint8, count=1)

    with rasterio.open(new_path, 'w', **meta) as dst:
        dst.write(output, 1)

    print(f"Imagem processada salva em: {new_path}")
    return output
