from flask import Flask, request, jsonify
from models.transaction import Transaction
from schemas.transaction import TransactionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


transaction_list = TransactionSchema(many=True)
def transaction_routes(app: Flask):

    @app.route('/transactions', methods=['POST'])
    @jwt_required()
    def register_transaction():
        try:
            if get_jwt_identity()["user_type"].lower() == "comprador":
                body = request.json

                new_transaction = Transaction(get_jwt_identity()["id"], body["seller_id"], body["item_id"], body["price"])

                new_transaction.add_transaction()

                return jsonify({"message": "Transacao cadastrado com sucesso."}), 201
            else:
                return jsonify({"message": "Apenas compradores tem permissao para efetuar transacoes."}), 403
        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    @app.route('/transactions/<int:id>', methods=['GET'])
    @jwt_required()
    def get_user_transactions(id):
        try:
            user_type = get_jwt_identity()["user_type"].lower()
            if ((user_type == "comprador" and get_jwt_identity()["id"] == id) or (user_type == "admin")):
                
                return jsonify(transaction_list.dump(Transaction.get_transaction_by_buyerid(id))), 200
            else:
                return jsonify({"message": "Apenas o titular da transacao e o admin tem acesso."}), 403
        
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    