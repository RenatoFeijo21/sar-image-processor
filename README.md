# SAR Image Processor

![Architecture](docs/architecture.png)

Software para processamento de imagens SAR com:

- Interface gráfica (PyQt5)
- Geração de histograma (Normal, Gama, K-distribution)
- CFAR 5x5 (99.5%)
- Estatísticas (média, variância, desvio, ENL)
- Máscara ROI (shapefile)
- Suporte Sentinel-1 e ICEYE

## 🚀 Instalação

```bash
git clone https://github.com/RenatoFeijo21/sar-image-processor.git
cd sar-image-processor
pip install -r requirements.txt
