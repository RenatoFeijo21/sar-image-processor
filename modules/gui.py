import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QLabel, QVBoxLayout, QWidget
import rasterio
import matplotlib.pyplot as plt
from modules import pre_processing, cfar, roi

class SARProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SAR Image Processor')
        self.image = None
        self.initUI()

    def initUI(self):
        menuInicio = self.menuBar().addMenu('Início')
        abrirAction = QAction('Abrir Imagem', self)
        abrirAction.triggered.connect(self.abrirImagem)
        menuInicio.addAction(abrirAction)

        sairAction = QAction('Sair', self)
        sairAction.triggered.connect(self.close)
        menuInicio.addAction(sairAction)

        menuPre = self.menuBar().addMenu('Pré-Processamento')
        histAction = QAction('Gerar Histograma', self)
        histAction.triggered.connect(self.histograma)
        menuPre.addAction(histAction)

        estatAction = QAction('Estatísticas', self)
        estatAction.triggered.connect(self.estatisticas)
        menuPre.addAction(estatAction)

        roiAction = QAction('Inserir Máscara ROI', self)
        roiAction.triggered.connect(self.inserirROI)
        menuPre.addAction(roiAction)

        menuProc = self.menuBar().addMenu('Processamento')
        cfarAction = QAction('CFAR 5x5', self)
        cfarAction.triggered.connect(self.cfar)
        menuProc.addAction(cfarAction)

        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrirImagem(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Abrir Imagem SAR', '', 'GeoTIFF (*.tif *.tiff)')
        if fileName:
            with rasterio.open(fileName) as src:
                self.image = src.read(1)
            plt.imshow(self.image, cmap='gray')
            plt.title('Imagem SAR')
            plt.show()

    def histograma(self):
        if self.image is not None:
            pre_processing.gerar_histograma(self.image)

    def estatisticas(self):
        if self.image is not None:
            media, var, desvio, enl = pre_processing.calcular_estatisticas(self.image)
            print(f'Média: {media}, Variância: {var}, Desvio: {desvio}, ENL: {enl}')

    def inserirROI(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Abrir ROI', '', 'Shapefile (*.shp)')
        if fileName:
            mask = roi.gerar_mascara_roi(fileName)
            plt.imshow(mask, cmap='gray')
            plt.title('Máscara ROI')
            plt.show()

    def cfar(self):
        if self.image is not None:
           result = cfar.cfar_process(self.image_path)
            plt.imshow(result, cmap='gray')
            plt.title('CFAR Processado')
            plt.show()
