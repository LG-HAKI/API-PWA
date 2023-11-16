from flask import Flask, request, jsonify
from models.item import Item
from schemas.item import ItemSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

item_list = ItemSchema(many=True)
item = ItemSchema()

def item_routes(app: Flask):

    @app.route('/items', methods=['GET'])
    def get_items():
        try:
            items = Item.get_items()
            return jsonify(item_list.dump(items)), 200
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/items', methods=['POST'])
    @jwt_required()
    def add_item():
        try:
            if get_jwt_identity()["user_type"].lower() == "vendedor":
                body = request.json

                new_item = Item(body["title"].lower(), body["author"].lower(), body["category_id"], body["price"], body["description"], body["edition_dt"], body["freq"], get_jwt_identity()["id"])
                new_item.add_item()

                return jsonify({"mensagem": "Item cadastrado com sucesso"}), 201
            
            else:
                return jsonify({"mensagem": "Apenas os usuários com privilégios de vendedor podem adicionar itens"}), 400
            
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/items/<int:id>', methods=['GET'])
    def get_item_details(id):
        try:
            item_details = Item.get_item_by_id(id)
            return jsonify(item.dump(item_details)), 200
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/items/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_item(id):
        try:
            body = request.json
            item = Item.get_item_by_id(id)
            seller_id = item.seller_id
            user_type = get_jwt_identity()["user_type"].lower()
            

            if ((user_type == "vendedor" and get_jwt_identity()["id"] == seller_id) or (user_type == "admin")):

                if item:
                    if body.get("price") or body.get("freq"):
                        
                        if body.get("price"):
                            price = body["price"]
                        else:
                            price = item.price
                        
                        if body.get("freq"):
                            freq = body["freq"]
                        else:
                            freq = item.frequency
                    else:
                        return jsonify({"mensagem": "Os dados não foram informados."}), 400
                    
                    item.update_item(price, freq)

                    return jsonify({"mensagem": "Dados atualizados com sucesso"}), 200
                else:
                    return jsonify({"mensagem": "Item não encontrado"}), 404
            else:
                return jsonify({"mensagem": "Apenas os vendedores que cadastraram o item e os administrados tem acesso."}), 403
            
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/items/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_item(id):
        try:
            item = Item.get_item_by_id(id)
            user_type = get_jwt_identity()["user_type"].lower()
            seller_id = item.seller_id

            if ((user_type == "vendedor" and get_jwt_identity()["id"] == seller_id) or (user_type == "admin")):
                item = Item.get_item_by_id_in_stock(id)
                
                if item:
                    item.delete_from_db()
                    return jsonify({"mensagem": "item removido com sucesso"}), 200
                else:
                    return jsonify({"mensagem": "Item não encontrado"}), 404

        except Exception as e:
            return jsonify({"Error": str(e)}), 500   

