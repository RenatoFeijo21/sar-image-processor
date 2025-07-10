import numpy as np

def cfar_process(image, k=3.29, win=2):
    rows, cols = image.shape
    output = np.zeros_like(image)

    for i in range(win, rows - win):
        for j in range(win, cols - win):
            window = image[i-win:i+win+1, j-win:j+win+1].flatten()
            guard = image[i,j]
            mean = np.mean(window)
            std = np.std(window)
            threshold = mean + k * std

            output[i,j] = 255 if guard > threshold else 0

    return output
