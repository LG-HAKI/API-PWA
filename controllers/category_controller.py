from flask import Flask, request, jsonify
from models.category import Category
from schemas.category import CategorySchema
from flask_jwt_extended import jwt_required, get_jwt_identity

category_list = CategorySchema(many=True)
category = CategorySchema()

def category_routes(app: Flask):

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.get_categories()
        return jsonify(category_list.dump(categories)), 200
        

    @app.route('/categories', methods=['POST'])
    @jwt_required()
    def add_category():
        try:
            if get_jwt_identity()["user_type"].lower() == "admin":
                body = category.load(request.json)

                new_category = Category(body.name.lower(), body.description)

                new_category.add_category(body.name.lower())

                return jsonify({"message": "Categoria cadastrado com sucesso."}), 201
            else:
                return jsonify({"message": "Apenas administradores têm permissão para cadastrar categorias."}), 403

        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500


    @app.route('/categories/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_category(id):
        try:
            if get_jwt_identity()["user_type"].lower() == "admin":
                body = request.json

                if body.get("name") or body.get("description"):
                    category_instance = Category.get_category_by_id(id)

                    if body.get("name"):
                        name = body["name"].lower()
                    else:
                        name = category_instance.name
                    
                    if body.get("description"):
                        description = body["description"]
                    else:
                        description = category_instance.description
                else:
                    return jsonify({"message": "Os dados não foram informados."}), 400

                category_instance.update_category(name, description)

                return jsonify({"message": "Categoria atualizada com sucesso."}), 201
            else:
                return jsonify({"message": "Apenas administradores têm permissão para atualizar categorias."}), 403
        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/categories/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_category(id):
        try:
            if get_jwt_identity()["user_type"] == "admin":
                category_instance = Category.get_category_by_id(id) 

                if category_instance:
                    category_instance.delete_from_db()
                    return jsonify({"message": "Categoria removida com sucesso."}), 200
                else:
                    return jsonify({"message": "Categoria não encontrado."}), 404
            else:
                return jsonify({"message": "Apenas administradores têm permissão para remover categorias."}), 403
        
        except Exception  as e:
            return jsonify({"Error": str(e)}), 500
