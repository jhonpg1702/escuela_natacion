# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.clients import blueprint
from flask import render_template, request,jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.clients.models import *

@blueprint.route('/list_clients')
@login_required
def list_clients():

    return render_template('clients/list_clients.html')

@blueprint.route("/dataClients", methods=["GET", "POST"])
@login_required
def dataClients():

    consult = Clients.query.all()

    data_json = []

    data_json = [
        {
            'id': item.id,
            'names': item.first_name +" "+item.second_name,
            'surnames': item.first_last_name + " " + item.second_last_name,
            'document': item.document,
            'age': item.age,
            'addres': item.addres,
            'phone': item.phone,
            'state': 'activado' if item.state else 'desactivado',  # Usando una expresión condicional
            'medicall_info': item.medicall_info,
            'email': item.email,
        } for item in consult
    ]

    # Retornar la data en formato JSON
    return jsonify({'data': data_json})


@blueprint.route('/create_client', methods=['POST'])
@login_required
def create_client():
    # Obtener los datos en formato JSON de la solicitud
    data = request.get_json()

    # Obtener los campos específicos del formulario
    first_name = data.get('first_name')
    second_name = data.get('second_name')
    first_last_name = data.get('first_last_name')
    second_last_name = data.get('second_last_name')
    document = data.get('dni')
    age = data.get('age')
    addres = data.get('addres')
    phone = data.get('phone')
    medicall_info = data.get('medicall_info')
    email = data.get('email')

    # Verificar si el cliente ya existe en la base de datos usando el número de teléfono
    existing_customer = Clients.query.filter_by(phone=phone).first()

    # Si el cliente ya existe, retornar un mensaje de error y el código 400
    if existing_customer:
        return jsonify({'tipo': "error", 'message': 'Ya existe un cliente con el mismo número de teléfono.'}), 400

    # Crear un nuevo cliente con los datos proporcionados
    cliente_form = Clients(
        first_name=first_name,
        second_name=second_name,
        first_last_name=first_last_name,
        second_last_name=second_last_name,
        document=document,
        age=age,
        addres=addres,
        phone=phone,
        medicall_info=medicall_info,
        email=email,
    )
    
    # Agregar el nuevo cliente a la sesión de la base de datos
    db.session.add(cliente_form)
    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Retornar un mensaje de éxito en formato JSON
    return jsonify({'tipo': "success", 'message': 'Cliente creado correctamente'}), 200


# get obtener la iformacion del cliente atraves del id 
@blueprint.route('/get_customer/<id>', methods=['GET', 'POST'])
def get_customer(id):
    # Buscar en la base de datos el cliente con el id proporcionado
    consult = Clients.query.filter_by(id=id).first()

    if consult:
        # Si el cliente es encontrado, crear un diccionario con sus datos
        data_json = {
            'id': consult.id,
            'first_name': consult.first_name,
            'second_name': consult.second_name,
            'first_last_name': consult.first_last_name,
            'second_last_name': consult.second_last_name,
            'document': consult.document,
            'age': consult.age,
            'addres': consult.addres,
            'phone': consult.phone,
            'estate': consult.state,
            'medicall_info': consult.medicall_info,
            'email': consult.email,
        }
        # Retornar los datos del cliente en formato JSON
        return jsonify(data_json)
    else:
        # Si no se encuentra el cliente con el ID dado, retornar un mensaje de error y el código 404
        return jsonify({'error': 'Cliente no encontrado'}), 404

    
@blueprint.route('/edit_customer', methods=['POST'])
def edit_customer():
    # Obtener los datos en formato JSON de la solicitud
    data = request.get_json()
    # Obtener el 'id' del cliente de los datos proporcionados
    id = data.get('id')

    # Obtener los demás campos del formulario
    first_name = data.get('first_name')
    second_name = data.get('second_name')
    first_last_name = data.get('first_last_name')
    second_last_name = data.get('second_last_name')
    document = data.get('dni')
    age = data.get('age')
    addres = data.get('addres')
    phone = data.get('phone')
    medicall_info = data.get('medicall_info')
    email = data.get('email')

    # Buscar en la base de datos el cliente con el id proporcionado
    consult = Clients.query.filter_by(id=id).first()

    # Actualizar los campos del cliente con los valores proporcionados
    consult.first_name = first_name
    consult.second_name = second_name
    consult.first_last_name = first_last_name
    consult.second_last_name = second_last_name
    consult.document = document
    consult.age = age
    consult.addres = addres
    consult.phone = phone
    consult.medicall_info = medicall_info
    consult.email = email

    # Confirmar los cambios en la base de datos
    db.session.commit()
    
    # Retornar un mensaje de éxito en formato JSON
    return jsonify({'success': True})


@blueprint.route('/edit_state_client', methods=['GET','POST'])
@login_required
def edit_state_client():
    try:
        # Intentar obtener los valores 'id' y 'state' desde el formulario enviado
        id = request.form['id']
        state = request.form['state']
        
        # Buscar en la base de datos el cliente con el id proporcionado
        consult = Clients.query.filter_by(id=id).first()

        # Si no se encuentra el cliente, retornar un mensaje de error 
        if not consult:
            return jsonify({'tipo': 'error', 'message': 'Cliente no encontrado'}), 404

        tipo = ""
        message = ""

        # Verificar el estado recibido y actualizar el estado del cliente en la base de datos
        if state == "0":
            consult.state = False  # Desactivar cliente
        elif state == "1":
            consult.state = True   # Activar cliente
        else:
            # Si el estado no es válido, retornar un mensaje de error
            return jsonify({'tipo': 'error', 'message': 'Estado inválido'}), 400

        # Confirmar los cambios en la base de datos
        db.session.commit()

        tipo = "success"
        # Crear el mensaje de éxito según el estado proporcionado
        message = f"Se {'activó' if state == '1' else 'desactivó'} el cliente correctamente"

        # Retornar el mensaje de éxito en formato JSON
        return jsonify({'tipo': tipo, 'message': message})

    except KeyError as e:
        # Manejo de errores por campos faltantes en request.form
        return jsonify({'tipo': 'error', 'message': f'Falta el campo {str(e)}'}), 400
