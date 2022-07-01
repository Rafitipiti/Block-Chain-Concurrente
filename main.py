from hashlib import sha256
import hashlib
import json
import time
from urllib import response
from uuid import uuid4
from urllib.parse import urlparse
import requests

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
PoW = 4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current = []
        self.nodes = set()

        self.newBlock(previous_hash=0, proof=0)
    
    def registerNode(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def isValid(self, chain):
        lblock = chain[0]
        curr = 1

        while curr < len(chain):
            block = chain[curr]

            if block['previous_hash'] != self.hash(lblock):
                return False 
            
            if not self.valid_proof(lblock['proof'], block['proof']):
                return False
            
            lblock = block 
            curr+= 1
        
        return True
    
    def solve(self):
        nexts = self.nodes
        nchain = None

        mx = len(self.chain)

        for node in nexts:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                ln = response.json()['length']
                chain = response.json()['chain']

                if ln > mx and self.isValid(chain):
                    mx = ln
                    nchain = chain
        
        if nchain:
            self.chain = nchain
            return True


    def newBlock(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current = []
        self.chain.append(block)

        return block

    def newTransaction(self, sender, recipient, amount):
        self.current.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,

        })

        return self.lastBlock['index'] + 1

    @staticmethod
    def hash(block):
        bst = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(bst).hexdigest()

    @property
    def lastBlock(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof+= 1

        return proof 
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        ghash = hashlib.sha256(guess).hexdigest()
        return ghash[:PoW] == PoW*"0"
    

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/minar', methods=['GET'])
def mine():
    lblock = blockchain.lastBlock
    lproof = lblock['proof']
    proof = blockchain.proof_of_work(lproof)

    blockchain.newTransaction(0,node_identifier,1)

    prevhash = blockchain.hash(lblock)
    block = blockchain.newBlock(proof, prevhash)

    response = {
        'mensaje': 'nuevo bloque agregado',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/transaccion/nueva', methods=['POST'])
def new_transaction():
    data = request.get_json()
    fields = ['sender', 'recipient', 'amount']
    for f in fields:
        if not data.get(f):
            return "data invalida", 404
    
    index = blockchain.newTransaction(data['sender'], data['recipient'], data['amount'])
    
    return "agregando nueva transaccion a bloque " + str(index), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'tamaño': len(blockchain.chain),
    }

    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error en lista de nodos", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Se agregaron los nuevos nodos',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    ok = blockchain.resolve_conflicts()

    if not ok:
        response = {
            'message': 'La cadena fue remplazada',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'La cadena es autoritativa',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run()
