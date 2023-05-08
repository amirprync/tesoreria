from flask import Flask, request, send_file, render_template
import pandas as pd
import os
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            df = pd.read_excel(file, engine='openpyxl')
            output = StringIO()

            for _, fila in df.iterrows():
                cbu = str(int(fila['CBU']))
                cuit = str(int(fila['CUIT']))
                nombre = str(fila['NOMBRE'])
                importe = str(fila['IMPORTE'])

                registro = f'DR2;900100000102553;{cbu};;{cuit};{nombre};{importe};VAR;N;N;TRANSF COHEN;\n'
                output.write(registro)

            output.seek(0)
            return send_file(output, as_attachment=True, attachment_filename='salida.txt', mimetype='text/plain')

    return '''
    <!doctype html>
    <title>Generador de Archivo TXT desde Excel</title>
    <h1>Sube tu archivo Excel</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Subir>
    </form>
    '''

if __name__ == '__main__':
    import os
from werkzeug.serving import run_simple
app.run(debug=True)
import os
import threading
from werkzeug.serving import run_simple

def run_app():
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        run_simple('localhost', 5000, app, use_debugger=True, use_reloader=False)
    else:
        app.run(debug=True)

if __name__ == '__main__':
    t = threading.Thread(target=run_app)
    t.start()


