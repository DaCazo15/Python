import os
import comtypes.client

def word_to_pdf(carpeta):
    # Crear una instancia de Word
    word = comtypes.client.CreateObject("Word.Application")
    word.Visible = False  # Ocultar la ventana de Word
    # Recorrer todos los archivos de la carpeta
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".docx"):  # Filtrar archivos .docx
            ruta_docx = os.path.abspath(os.path.join(carpeta, archivo))
            ruta_pdf = os.path.abspath(os.path.join(carpeta, archivo.replace(".docx", ".pdf")))  # Ruta completa del archivo de salida
            try:
                # Abrir el archivo .docx
                doc = word.Documents.Open(ruta_docx)
                # Guardar como PDF
                doc.SaveAs(ruta_pdf, FileFormat=17)  # 17 es el formato para PDF
                doc.Close()
                print(f"Convertido: {archivo} -> {ruta_pdf}")
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")
        os.remove(ruta_docx)
    word.Quit()