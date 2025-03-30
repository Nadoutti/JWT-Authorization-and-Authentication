from flask import Flask, request, jsonify, redirect
import jwt
from conn_db import conn_db

app = Flask(__name__)


# criando a rota principal para o server
@app.route('/')
def index():
    return jsonify({'mensagem': 'servidor rodando :)'})



# fazendo a rota de login
@app.route('/login', methods=['POST'])
def login():

    #configs basicas
    key = "chave"
    response = request.get_json()
    connection = conn_db()
    cursor = connection.cursor()

    
    # tokenizando as informacoes do usuario
    encoded_password = jwt.encode({"password": response['senha']}, key, algorithm="HS256")
    print(encoded_password)
    print(type(encoded_password))
    print(len(encoded_password))
    cursor.execute(f" SELECT * FROM tbl_usuarios WHERE PASSWORD = ? ", (encoded_password,))

    dados_usuario = cursor.fetchone()
    if dados_usuario:
        cursor.execute('''
            UPDATE tbl_usuarios SET AUTHORIZED = '1' WHERE PASSWORD = ?
        ''', (encoded_password,))
        connection.commit()
        connection.close()
        return redirect('/'), 200

    cursor.close()
    connection.close()

    return jsonify({"mensagem": "deu problema"})


# fazer o signin
@app.route('/signin', methods=['POST'])
def signin():
    key = "chave"
    response = request.get_json()
    connection = conn_db()
    cursor = connection.cursor()

    # tokenizando as informacoes do usuario
    encoded_password = jwt.encode({"password": response['senha']}, key, algorithm="HS256")
    encoded_email = jwt.encode({"email": response['email']}, key, algorithm="HS256")


    cursor.execute('''
        INSERT INTO tbl_usuarios (EMAIL, PASSWORD, NOME) VALUES (?, ?, ?)
    ''', (encoded_email, encoded_password, response['nome']))

    if cursor.rowcount > 0:
        connection.commit()
        connection.close()
        return redirect('/login'), 200

    return jsonify({"erro": "houve um erro ao fazer signin"})

if __name__ == "__main__":
    app.run()
