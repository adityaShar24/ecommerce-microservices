from flask import Blueprint, request, jsonify
from .middleware import token_required
from .models import db, User, Address, UserSchema, AddressSchema

bp = Blueprint('routes', __name__)
user_schema = UserSchema()
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

@bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return user_schema.jsonify(user)

@bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.full_name = data.get('full_name', user.full_name)
    user.phone = data.get('phone', user.phone)
    db.session.commit()
    return user_schema.jsonify(user)

@bp.route('/users/<int:user_id>/addresses', methods=['POST'])
@token_required
def add_address(user_id):
    data = request.json
    address = Address(
        user_id=user_id,
        address_line=data['address_line'],
        city=data['city'],
        state=data['state'],
        zipcode=data['zipcode'],
        country=data['country']
    )
    db.session.add(address)
    db.session.commit()
    return address_schema.jsonify(address), 201

@bp.route('/users/<int:user_id>/addresses', methods=['GET'])
@token_required
def get_addresses(user_id):
    addresses = Address.query.filter_by(user_id=user_id).all()
    return addresses_schema.jsonify(addresses)

@bp.route('/addresses/<int:address_id>', methods=['PUT'])
@token_required
def update_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    data = request.json
    address.address_line = data.get('address_line', address.address_line)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.zipcode = data.get('zipcode', address.zipcode)
    address.country = data.get('country', address.country)
    db.session.commit()
    return address_schema.jsonify(address)

@bp.route('/addresses/<int:address_id>', methods=['DELETE'])
@token_required
def delete_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    db.session.delete(address)
    db.session.commit()
    return jsonify({"message": "Address deleted successfully"})
