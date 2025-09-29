from flask import request, jsonify, render_template 
from app import app                                   
from services.usuario_service import cadastrar_usuario


# Rota de Cadastro de Usuário
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def rota_cadastro_usuario():
    if request.method == 'POST':
        try:
            # 🔹 Captura os dados enviados pelo formulário
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')  # se houver senha, criptografe antes de salvar!

            # 🔹 Chama o service responsável por cadastrar o usuário
            cadastrar_usuario(nome, email, senha)

            return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

        except ValueError as ve:
            # Erros de validação (ex.: email inválido, nome vazio, etc.)
            return jsonify({"message": str(ve)}), 400

        except Exception as e:
            # Erros inesperados no banco ou no backend
            return jsonify({"message": "Erro ao cadastrar usuário."}), 500

    # 🔹 Para requisições GET, apenas renderiza a página do painel ou formulário
    return render_template('painel_admin.html')
