#this is my first blockchain project
import hashlib
import datetime
import json
from flask import Flask,jsonify

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,prevhash='0000')
        #we make this in constructor coz before we mine any block genesis block shuld exist
        
    def create_block(self,proof,prevhash):
        time=str(datetime.datetime.now())
        block={"index":len(self.chain)+1,"timestamp":time,"prevhash":prevhash,"proof":proof}
        self.chain.append(block)
        return(block)
    
    def prev_block(self):
        return self.chain[-1]
    
    #def hash(self,block,prevblock):
      #  newproof=block["proof"]
       # prevproof=prevblock["proof"]
        #hash=hashlib.sha256(str(newproof**2-prevproof**2).encode()).hexdigest()
        #return hash
        
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()#?????????
        
        
    
    def proof_of_work(self):
        check=False
        newproof=1
        prevproof=prev_block()["proof"]
        while check==False:
            hash=hashlib.sha256(str(newproof**2-prevproof**2).encode()).hexdigest()#any other function for sha may lead to duplication of hash
            #addition is symmetrical as newproof=2 or 3,prevproof=3 or 2 thus same hash for both situation(new+prev)
            if(hash[:4]=='0000'):
                check=True
            else:
                newproof+=1
        return newproof
    
    def is_chain_valid(self):#two checks
        #1. whether previous hash is right mentioned 
        #2. validate nonce or proof of work
        #we are finding prev hash is right or not ,for prev hash we need prev proof
        prevblock=chain[0]
        ctr=0
        while(ctr<len(chain)):
            block=chain[ctr+1]
            prevhash=hash(prevblock)#ye prevblock ka hai toh prevproof isse bhi previous
            if(prevhash!=block["prevhash"]):
                return False
                #hash property satisfied now go for next property
            hash=hash(block)##########?
            if(hash[:4]!='0000'):
                return False
                
            ctr+=1
            #prevblock=prev_block()#this is wrong this will give the last block of the chain but we need next prev to our current iteration
            prevblock=block
        return True
           
        
        #self.hash kyun aur self.chain kyun nhi???
        

        
#create an app
app=Flask(__name__)
blockchain=Blockchain()

#mining a block
@app.route('/miningtheblock',methods=['GET'])
def miningtheblock():
    prevblock=blockchain.prev_block()
    #prevhash=prevblock["hash"] #we cant do this as this will give prev hash of prev block but we want hash not prev hash of prev block
    prevhash=blockchain.hash(prevblock)
    proof=blockchain.proof_of_work()
    block=blockchain.create_block(proof,prevhash)
    response={'message':'Congrats you just mined a block','index':block["index"],'timestamp':block["time"],'proof':block["proof"],'prevhash':block["prevhash"]}
    return jsonify(response),200
        
#display the whole blockchain
@app.route('/viewtheblockchain',methods=['GET']) 
def viewtheblockchain():  
    response={'chain':blockchain.chain,'length':length(blockchain.chain)}
    return jsonify(response),200

#validate the whole blockchain
@app.route('/validatetheblockchain',methods=['GET'])
def validatetheblockchain():
    if blockchain.is_chain_valid():
        reponse={'message':'all good,blockchain is valid'}
    else:
        reponse={'message':'We have a problem blockchain is not working fine'}
        return jsonify(response),200#port 200 means ok recieved,It means the action was successfully received, understood, and accepted
    
#runnning the app
app.run(host='0.0.0.0',port=5000)#check and run on other systems in your network
#there are 64 bits only in prev hash?????????????????????