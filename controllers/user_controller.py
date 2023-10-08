from flask import Flask, request, jsonify
from models.user import User
from schemas.user import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.bcrypt_util import generate_password_hash, check_password
from utils.validation_util import validate_email
from datetime import date

user_schema = UserSchema()

def user_routes(app: Flask):

    
    @app.route('/users/signup', methods=['POST'])
    def user_signup():
        try:
            body = user_schema.load(request.json)
            
            password_hash = generate_password_hash(body.password)
            
            if password_hash:
                body.password = password_hash
            else:
                return jsonify({
                    "mensagem": "A password não respeita o padrão exigido."
                }), 400

            if not validate_email(body.email):
                return jsonify({
                    "mensagem": "O email não respeita o padrão exigido."
                }), 400

            if not body.user_type.lower() in ["comprador", "vendedor"]:
                return jsonify({
                    "mensagem": "O user_type não respeita o padrão exigido."
                }), 400
            
            
            new_user = User(body.name, body.email, body.password, body.user_type)

            new_user.save_to_db()

            return jsonify({"message": "Usuário cadastrado com sucesso."}), 201
        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        


    @app.route('/users/login', methods=['POST'])
    def user_login():
        body = request.json

        if not (body.get("email") and body.get("password")):
            return jsonify({"message": "Email e/ou password não foram devidamente informados."}), 400

        user_info = User.get_user_info(body["email"])
        
        if user_info:

            if user_info[2].lower() in ["comprador", "vendedor"]:

                if check_password(user_info[1], body["password"]):
                    access_token = create_access_token(identity={"id": user_info[0], "user_type": user_info[2]})
                    return jsonify(
                        {
                            "message": "Login efetuado com sucesso.",
                            "acess_token": access_token
                        }

                    ), 200
                
                else:
                    return jsonify({"message": "Email e/ou password informados são inválidos"}), 401
            
            else:
                return jsonify({"message": "Rota destinada ao login exclusivo de compradores e vendedores."}), 401
            
        else:
            return jsonify({"message": "Email e/ou password informados são inválidos"}), 401
            
        

    #finalizado
    @app.route('/users/<int:id>', methods=['PUT'])
    @jwt_required()
    def user_update(id):
        try:
            if get_jwt_identity()["user_type"] == "admin":
                
                body = request.json

                if body.get("name") or body.get("password"):

                    user = User.get_user_by_id(id)

                    if body.get("password"):
                        password_hash = generate_password_hash(body["password"])
                    else:
                        password_hash = user.password

                    user.user_update(body["name"], password_hash)

                    return jsonify({"message": "Dados do usuário foram atualizados com sucesso."}), 200
                
                else:
                    return jsonify({"message": "Os campos de mudança não foram devidamente informados."}), 400

            else:
                return jsonify({"message": "Apenas administradores têm permissão para editar usuários."}), 403
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    #finalizado
    @app.route('/users/<int:id>', methods=['DELETE'])
    @jwt_required()
    def user_delete(id):
        try:
            if get_jwt_identity()["user_type"] == "admin":
                user = User.get_user_by_id(id)
                if user:
                    user.delete_from_db()
                    return jsonify({"message": "Usuário removido com sucesso."}), 200
                else:
                    return jsonify({"message": "Usuário não encontrado."}), 404
            else:
                return jsonify({"message": "Apenas administradores têm permissão para editar usuários."}), 403
        
        except Exception  as e:
            return jsonify({"Error": str(e)}), 500


