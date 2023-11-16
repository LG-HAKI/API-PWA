from flask import Flask, request, jsonify
from models.user import User
from schemas.user import UserSchema
from utils.bcrypt_util import generate_password_hash, check_password
from utils.validation_util import validate_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

admin = UserSchema()
admin_list = UserSchema(many=True)

def admin_routes(app: Flask):

    @app.route('/admin/signup', methods=['POST'])
    @jwt_required()
    def admin_signup():
        try:
            if get_jwt_identity()["user_type"] == "admin":
                body = admin.load(request.json)
                
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

                if not body.user_type.lower() == "admin":
                    return jsonify({
                        "mensagem": "O user_type não respeita o padrão exigido."
                    }), 400
                
                if body.expertise:
                    expertise = body.expertise
                else:
                    expertise = None
                
                new_admin = User(body.name, body.email, body.password, body.user_type, expertise)

                new_admin.save_to_db()

                return jsonify({"message": "Admin cadastrado com sucesso."}), 201
            else:
                return jsonify({"message": "Apenas administradores podem cadastrar administradores."}), 403
        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/admin/login', methods=['POST'])
    def admin_login():
        
        try:
            body = request.json

            if not (body.get("email") and body.get("password")):
                return jsonify({"message": "Email e/ou password não foram devidamente informados."}), 400

            user_info = User.get_user_info(body["email"])
            
            if user_info:

                if user_info[2].lower() == "admin":

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
                    return jsonify({"message": "Rota destinada ao login exclusivo de administradores."}), 401
                
            else:
                return jsonify({"message": "Email e/ou password informados são inválidos"}), 401
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    #finalizada 
    @app.route('/admin/reports', methods=['GET'])
    @jwt_required()
    def get_reports():
        try:
            if get_jwt_identity()["user_type"] == "admin":
                comp, vend, admin, inat = User.get_count_users_type()
                
                return jsonify({
                    'numero_compradores': comp,
                    'numero_vendedores': vend,
                    'numero_admin': admin,
                    'numero_usuarios_inativos': inat
                }), 200
            else:
                return jsonify({"message": "Apenas administradores têm acesso as estatísticas."}), 403
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    #finalizada 
    @app.route('/admin/users', methods=['GET'])
    @jwt_required()
    def get_users():
        try:
            if get_jwt_identity()["user_type"] == "admin":
                user_list = User.get_users()
                return jsonify(admin_list.dump(user_list)), 200
            else:
                return jsonify({"message": "Apenas administradores têm permissão para editar usuários."}), 403
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
