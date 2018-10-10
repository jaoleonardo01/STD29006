#!/usr/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)

livros = [
	{	
	'id': 1,
	'titulo':'Linguagem de Programacao C',
	'autor':'Dennis Ritchie'
	}
]

#
@app.route('/livros', methods=['GET'])
def obtem_livros():
	return jsonify({'livros': livros})
# Como invocar na linha de comando
#
# curl -i http://localhost:5000/livros/1
#
@app.route('/livros/<int:idLivro>', methods=['GET'])
def detalhe_livro(idLivro):
	resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
	if len(resultado) == 0:
		abort(404)
	return jsonify({'livro': resultado[0]})
# Como invocar na linha de comando
#
# curl -i -X DELETE http://localhost:5000/livros/2
#
@app.route('/livros/<int:idLivro>', methods=['DELETE'])
def excluir_livro(idLivro):
	resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
	if len(resultado) == 0:
		abort(404)
	livros.remove(resultado[0])
	return jsonify({'resultado': True})
# Como invocar na linha de comando
#
# curl -i -H "Content-Type: application/json" -X POST -d '{"titulo":"O livro","autor":"Joao"}'http://localhost:5000/livros
#
@app.route('/livros', methods=['POST'])
def criar_livro():
	if not request.json or not 'titulo' in request.json:
		abort(400)
	livro = {
		'id': livros[-1]['id'] + 1,
		'titulo': request.json['titulo'],
		'autor': request.json.get('autor', "")
	}
	livros.append(livro)
	return jsonify({'livro': livro}), 201
# Como invocar na linha de comando
#
# curl -i -H "Content-Type: application/json" -X PUT -d '{"titulo":"Novo Titulo"}' http://localhost:5000/livros/2
#
@app.route('/livros/<int:idLivro>', methods=['PUT'])
def atualizar_livro(idLivro):
	resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
	if len(resultado) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'titulo' in request.json and type(request.json['titulo']) != unicode:
		abort(400)
	if 'autor' in request.json and type(request.json['autor']) is not unicode:
		abort(400)
	resultado[0]['titulo'] = request.json.get('titulo', resultado[0]['titulo'])
	resultado[0]['autor'] = request.json.get('autor', resultado[0]['autor'])
	return jsonify({'livro': resultado[0]})
#### Autenticacao simples ####
# Como invocar na linha de comando
#
# curl -u aluno:senha123 -i http://localhost:5000/livrosautenticado
#
@app.route('/livrosautenticado', methods=['GET'])
@auth.login_required
def obtem_livros_autenticado():
	return jsonify({'livros': livros})
# Autenticacao simples
@auth.get_password
def get_password(username):
	if username == 'aluno':
		return 'senha123'
	return None
@auth.error_handler
def unauthorized():
	return make_response(jsonify({'erro': 'Acesso Negado'}), 403)
##############################
# Para apresentar erro 404 HTTP se tentar acessar um recurso que nao existe
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)


if __name__ == "__main__":
	print("Servidor no ar!")
	app.run(host='0.0.0.0',port='8000', debug=True)
