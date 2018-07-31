#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 07:29:35 2018

@author: thunderbolt
"""

# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
import requests
from uuid import uuid4
from urlparse import urlparse

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []#transactions should be before create block so that they can be added 
        self.transactions=[]#coz transactions should exist separately before we create a block this is called as mempool
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes=set()#these are the diff addresses of the systems to ensure decentralization,this will be a set
    
    def replace_chain(self):#this is to ensure consensus protocol-find the longest chain and inn all the nodes replace current by that one
        json=request.get_json()
        longest_chain_length=length(self.chain)
        replace_chain=self.chain
        for node in nodes:
            response=requests.get('http://{node}/get_chain'.format(node=node))# why http again??
            length_chain=response.json()['length']
            current_chain=response.json()['chain']
            if response == 200:#i.e.OK
                if length_chain > longest_chain_length and is_chain_valid(current_chain):
                    longest_chain_length=length_chain# by looping it through all the networks available we will find the max len
                    replace_chain=current_chain#this is the chain with longest length
                #replace_chain contains the longest chain
                # if longest chain is in the current node only no other node than also replace chain ahs longest chain
                self.chain=replace_chain #current chain becomes the longest
                return True
                
            return False
        
    
    def add_nodes(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)#note as nodes is an array so we cant use append here therefore add
        
    def add_transaction(self,sender,reciever,amount):
        transaction={'sender':sender,'reciever':reciever,'amount':amount}
        self.transactions.append(transaction)
        return len(self.chain)#this will return the index of the new block which is not yet mined,to be mined as this transaction is for the new block
        
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,'transaction':self.transaction}
        self.transaction=[]#once we loaded the mempool into the block it should get vacant as no two blocks can have same transaction
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

#adding the nodes in the network
@app.route('/add_nodes',methods=['POST'])
def add_nodes():
    json=requests.get_json()
    nodes=json.get['nodes']
    if(nodes is None):
        response={'message':'No node to connect'}
        return jsonify(response),400 #error message

    for node in nodes:
        blockchain.add_nodes(node)
    response={'message':'nodes are connected','totalnodes':length(blockchain.nodes)}
    return jsonify(response),201
    
    
    
#adding transactions to the block
@app.route('/add_transactions',methods=['POST'])
def add_transactions():
    json=requests.get_json()
    sender=json.get['sender']
    reciever=json.get['reciever']
    amount=json.get['amount']
    blockchain.add_transaction(sender,reciever,amount)
    response={'message':'transaction is added successfully',}
 
    
    
#replace the current chain with the longest chain
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    if replace_chain():#if true
        reponse={'message':'the chain is successfully replaced','chain':blockchain.chain,'chain_length':length(blockchain.chain)}
    else:
        reponse={'message':'houston we have a problem'}
    return jsonify(response),200
        

# Running the app
app.run(host = '0.0.0.0', port = 5001)
