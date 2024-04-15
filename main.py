from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar a tabela no banco de dados
def criar_tabela():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT NOT NULL,
                      destino TEXT NOT NULL,
                      peso REAL NOT NULL,
                      valor REAL NOT NULL)''')
    conn.commit()
    conn.close()

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para lidar com o formulário de envio de dados
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    criar_tabela()  # Chamada para garantir que a tabela exista
    nome = request.form['nome']
    destino = request.form['destino']
    peso = request.form['peso']
    valor = request.form['valor']

    # Salvar os dados no banco de dados
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO registros (nome, destino, peso, valor) VALUES (?, ?, ?, ?)', (nome, destino, peso, valor))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Rota para exibir os dados cadastrados
@app.route('/consultar')
def consultar():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    dados = cursor.fetchall()
    conn.close()

    return render_template('consultar.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)
