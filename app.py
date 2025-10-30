from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuração MySQL
db_config = {
    'host': 'paparella.com.br',
    'user': 'paparell_aluno_3',
    'password': '@Senai2025',
    'database': 'paparell_iot'
}

def get_connection():
    return mysql.connector.connect(**db_config)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Inserir ou atualizar LED
@app.route('/api/led', methods=['POST'])
def update_led():
    data = request.get_json()
    nome_aluno = data.get('nome_aluno')
    estado_led = data.get('estado_led')

    if not nome_aluno:
        return jsonify({'error': 'nome_aluno é obrigatório'}), 400

    try:
        estado_led = int(estado_led)
        if estado_led not in (0, 1):
            raise ValueError
    except:
        return jsonify({'error': 'estado_led inválido'}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_led FROM led WHERE nome_aluno = %s", (nome_aluno,))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE led SET estado_led = %s WHERE nome_aluno = %s", (estado_led, nome_aluno))
        else:
            cursor.execute("INSERT INTO led (nome_aluno, estado_led) VALUES (%s, %s)", (nome_aluno, estado_led))

        conn.commit()
        return jsonify({'message': 'LED registrado/atualizado com sucesso!'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro ao salvar no banco.'}), 500
    finally:
        cursor.close()
        conn.close()

# Buscar estado do LED de um aluno
@app.route('/api/led/<nome_aluno>', methods=['GET'])
def get_led(nome_aluno):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT estado_led FROM led WHERE nome_aluno = %s", (nome_aluno,))
        result = cursor.fetchone()
        if result:
            return jsonify({'estado_led': int(result['estado_led'])})
        else:
            return jsonify({'estado_led': 0})  # padrão desligado
    except Exception as e:
        print(e)
        return jsonify({'error': 'Erro ao buscar estado do LED.'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
