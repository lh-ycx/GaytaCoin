# -*- coding: UTF-8 -*-

import hashlib
import json
import decimal
import requests
from textwrap import dedent
from blockchain import Blockchain
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request, render_template
from flask_wtf import Form
from wtforms import StringField,SubmitField,DecimalField
from wtforms.validators import DataRequired
from blockchain import MyForm, Register_Form

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/login', methods=['POST'])
def get_openid():
    code = request.form['code']
    appid = 'wx8ae9681bcddfcdfe'
    secret = 'b871278e131917f8a793fdfb7c0ad0a9'
    wxurl = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid, secret, code)
    response = requests.get(wxurl)
    res = {}
    res['openid'] = json.loads(response.text)['openid']
    return jsonify(res)


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return render_template("mine.html", response_message=response)


@app.route('/transactions', methods=['GET','POST'])
def new_transaction():
    '''
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    '''
    form = MyForm(csrf_enabled=False)
    if form.validate_on_submit():
        amount = form.data['amount']
        index = blockchain.new_transaction(form.data['sender'], form.data['recipient'], int(amount))
        response = {'message': f'Transaction will be added to Block {index}'}
        return render_template("new_transaction.html",message=response)

    return render_template('new_transaction.html',form=form)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    
    return render_template("chain.html",chain=blockchain.chain,length=len(blockchain.chain))
    

@app.route('/pure_chain', methods=['GET'])
def pure_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/', methods=['GET'])
def hello():
    return render_template("index.html")


@app.route('/register', methods=['GET','POST'])
def register_nodes():
    '''
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201
    '''
    form = Register_Form(csrf_enabled=False)
    if form.validate_on_submit():
        node = form.data['node']
        blockchain.register_node(node)
        response = {'message': f'new node {node} has been recorded'}
        return render_template("register.html",message=response)

    return render_template('register.html',form=form)


@app.route('/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        message='Our chain was replaced'
    else:    
        message='Our chain is authoritative'        

    return render_template("resolve.html",message=message,chain=blockchain.chain)
    #return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
