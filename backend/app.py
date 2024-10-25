# app.py
from flask import Flask, request, render_template, jsonify
from cargar import cargar_mensajes
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta para almacenar el archivo subido

# Ruta de inicio para renderizar el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para cargar el archivo XML
@app.route('/cargar_xml', methods=['POST'])
def cargar_xml():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Guardar el archivo en el servidor temporalmente
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Procesar el archivo XML
    try:
        mensajes = cargar_mensajes(filepath)
        contenido = "\n".join(str(mensaje) for mensaje in mensajes)  # Convertir los mensajes en texto
    except Exception as e:
        return jsonify({"error": f"Error processing file: {e}"}), 500
    finally:
        os.remove(filepath)  # Eliminar el archivo después del procesamiento

    return jsonify({"contenido": contenido})

if __name__ == '__main__':
    app.run(debug=True)
