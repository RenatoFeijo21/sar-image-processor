from osgeo import gdal, ogr

def gerar_mascara_roi(shapefile_path):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapefile = driver.Open(shapefile_path, 0)
    layer = shapefile.GetLayer()
    print(f"ROI contém {layer.GetFeatureCount()} features.")
    # Para uso real, rasterizar em conjunto com imagem SAR carregada
    return None
