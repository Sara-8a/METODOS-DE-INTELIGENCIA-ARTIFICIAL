import yfinance as yf
import pandas as pd

def download_values(subyacente, start_date, end_date, fr='d', data_type='history'):
    """
    Descarga los valores históricos de un activo bursátil.
    
    Ejemplo de uso:
    res = download_values('GRUMAB.MX', '2016-05-26', '2017-07-05', 'd', 'history')
    """
    
    # Mapeo de las frecuencias del script original a la nomenclatura de yfinance
    # 'd' = daily, 'w'=weekly, 'm'= monthly
    freq_map = {'d': '1d', 'w': '1wk', 'm': '1mo'}
    interval = freq_map.get(fr.lower(), '1d')
    
    try:
        # Inicializar el objeto Ticker con el nombre del subyacente
        ticker = yf.Ticker(subyacente)
        if data_type == 'history': #
            # Descarga de datos históricos de precios
            hist = ticker.history(start=start_date, end=end_date, interval=interval)
            
            # Limpiar datos faltantes
            hist = hist.dropna()
            
            # Retornamos el DataFrame. Columnas incluidas: Open, High, Low, Close, Volume, Dividends, Stock Splits
            return hist
            
        elif data_type == 'div':  
            # Extraer solo los dividendos
            dividendos = ticker.dividends.loc[start_date:end_date]
            return dividendos.dropna()
            
        elif data_type == 'split':  
            # Extraer solo los splits
            splits = ticker.splits.loc[start_date:end_date]
            return splits.dropna()
            
        else:
            print("Advertencia: data_type no válido. Use 'history', 'div' o 'split'.")
            return None
            
    except Exception as e:
        # Equivalente al bloque catch: devuelve un objeto vacío y muestra el error
        print(f"Advertencia: Ocurrió un error al descargar los datos. Mensaje: {e}")  
        return pd.DataFrame() 

#####################################

# ==========================================
# Ejemplo de ejecución
# ==========================================
if __name__ == "__main__":
    # Descargar datos de Gruma S.A.B. de C.V.
    activo = download_values('GRUMAB.MX', '2016-05-26', '2017-07-05', 'd', 'history')  
    
    if not activo.empty:
        print("Datos descargados correctamente:")
        # Mostrar las primeras 5 filas (incluye la columna equivalente a adjclose)
        print(activo.head())
        
        
