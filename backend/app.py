from hashlib import sha256
import hashlib
import json
import time
from urllib import response
from uuid import uuid4
from urllib.parse import urlparse
from flask_cors import cross_origin
import requests
from flask import Flask, jsonify, request, send_from_directory, jsonify
from blockchain import *

app = Flask(__name__)

blockchain = Blockchain()
blockchain.create_genesis_block()

#miembros que participan del blockchain en la red =)
peers = set()

#UTILS - BLOCKCHAIN
def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain

def consensus():
    """
    Naive consensus algorithm. Sí se encuentra una cadena valida
    y más grande que la actual, entonces se reemplaza.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    """
    Método para anunciar a la red cuando un bloque ha sido minado.
    Otros bloques pueden verificar proof_of_work y añadirlo a sus cadenas.
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block.__dict__, sort_keys=True),
                      headers=headers)

#ENDPOINT PARA AGREGAR TRANSACCIONES
@app.route('/new_transaction', methods=['POST'])
@cross_origin()
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["from", "to","amount","currency"]
    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404
    tx_data["timestamp"] = time.time()
    blockchain.add_new_transaction(tx_data)
    return jsonify("Success",200)

#ENDPOINT PARA OBTENER LA CADENA QUE CONTIENE LA DATA
@app.route('/chain', methods=['GET'])
@cross_origin()
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return jsonify({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})


#ENDPOINT QUE EMPIEZA EL PROCESO DE MINADO A TRANSACCIONES NO CONFIRMADAS
@app.route('/mine', methods=['GET'])
@cross_origin()
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return jsonify("No transactions to mine")
    else:
        #OBTENER LA CADENA MÁS LARGA
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            #ANUNCIAR EL BLOQUE MINADO A LA RED
            announce_new_block(blockchain.last_block)
        return jsonify("Block #{} is mined.".format(blockchain.last_block.index))


#ENDPOINT PARA AGREGAR MIEMBROS A LA RED
@app.route('/register_node', methods=['POST'])
@cross_origin()
def register_new_peers():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return jsonify("Invalid data", 400)

    peers.add(node_address)

    return get_chain()


@app.route('/register_with', methods=['POST'])
@cross_origin()
def register_with_existing_node():
    """
    Llama al ENDOPOINT register_node para registrar
    el nodo actual en el nodo especificado en el request
    y sincronizar el blockchain
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return jsonify("Invalid data", 400)

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Registra la información en el nodo remoto y obtiene la información
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # actualiza la cadena y los miembros de la red
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return jsonify("Registration successful", 200)
    else:
        return jsonify(response.content, response.status_code)

# ENDPOINT PARA AGREGAR UN BLOQUE MINADO POR ALGUIEN MAS
# A LA CADENA DEL NODO. (VERIFICACION)
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


#ENDPOINT PARA OBTENER TRANSACCIONES PENDIENTES
@app.route('/pending_tx')
@cross_origin()
def get_pending_tx():
    return jsonify(blockchain.unconfirmed_transactions)

if __name__ == '__main__':
    app.run(debug=True, port=8000)