import hashlib
import json
from time import time

from urllib.parse import urlparse

import requests

class Blockchain(object):
    #생성자
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        self.nodes = set()

        # genesis block 생성
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        블록체인상에 새로운 블록을 만듭니다
        :파라미터 proof: <int> 작업 알고리즘의 증명
        :파리미터 previous_hash: (optional) <str> 이전 블록의 해시
        :반환값: <dict> 새로운 블록
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 거래의 현재 리스트를 초기화 
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        다음에 채굴될 블록에 추가될 새로운 거래를 만듭니다.
        :파라미터 sender: <str> Sender의 주소를 의미합니다.
        :파라미터 recipient: <str> Recipient의 주소를 의미합니다.
        :파라미터 amount: <int> 거래금액을 의미합니다.
        :return: <int> 트랜잭션에 대한 블록의 인덱스를 의미합니다.
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        블록의 SHA-256 해시를 생성
        :파라미터 block: <dict> 블록
        :리턴값: <str>
        """

        #딕셔너리를 정렬해야합니다. 그렇지 않으면 일치하지 않은 해시가 생깁니다.
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - hash(pp')가 선행되는 4개의 0을 가진 p'를 찾습니다. p는 p'이전의 작업 증명입니다.
         - p 는 이전 작업 증명이고, p'는 새로운 작업증명 입니다.
        :파리미터 last_proof: <int>
        :리턴값: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        """
        작업 증명의 유효성을 검사합니다: hash(last_proof, proof) 가 선행되는 4개의 0을 가지고 있는가?
        :파라미터 last_proof: <int> 이전 작업 증명
        :파리미터 proof: <int> 현재 작업증명
        :리턴값: <bool> True일때 맞음, False 일때 틀림.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"    


    def register_node(self, address):
        """
        노드의 리스트에 새로운 노드를 등록합니다.
        :파라미터 address: <str> 노드의 주소. Eg. 'http://127.0.0.1:8000/'
        :반환값: 없음
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    def valid_chain(self, chain):
        """
        블록체인이 유효한지를 결정합니다.
        :파라미터 chain: <list> 블록체인
        :리턴값: <bool> True 유효, False 유효하지 않음
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # 블록의 해시가 정확한지를 검사합니다.
            if block['previous_hash'] != self.hash(last_block):
                return False

            # 작업 증명이 정확한지를 검사합니다.
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):
        """
        이것이 우리의 합의 알고리즘 입니다, 
        네트워크상의 가장 긴 것과 교체함으로써 충돌을 해결합니다.
        :리턴값: <bool> True 우리의 체인이 교체되었습니다, False 교체되지 않았습니다.
        """

        neighbours = self.nodes
        new_chain = None
        
        # 우리의 체인보다 긴것만을 찾습니다.
        max_length = len(self.chain)

        # 우리의 네트워크 상의 모든 노드들로 부터 체인을 검사합니다.
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                #체인이 우리것보다 긴지 그리고 유효한지를 검사합니다.
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # 새로운 것을 발견하면 우리의 체인을 교체합니다. 유요한 체인은 우리의 체인보다 깁니다.
        if new_chain:
            self.chain = new_chain
            return True

        return False