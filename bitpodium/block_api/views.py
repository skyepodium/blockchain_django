from rest_framework.views import APIView
from rest_framework.response import Response

from blockchain.blockchain import Blockchain
from uuid import uuid4

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

class mine(APIView):
    def get(self, request):
        # 다음 증명을 위해 작업 증명 알고리즘을 수행합니다.
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        # 증명을 발견하는 것에 대해 반드시 보상을 받아야합니다.
        # sender가 0인것은 이 노드가 새로운 코인을 채울했음을 나타냅니다.
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        #새 블록을 체인에 추가하여 만듭니다.
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return Response(response, status = 200)


class new_transaction(APIView):

    def post(self, request):

        values = request.data
        print(values)
        #post 메소드에 들어있는 데이터 필드 확인
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return Response({'message': 'Missing values'}, status = 400)

        # 새로운 트랜잭션 생성
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        return Response({'message': f'Transaction will be added to Block {index}'}, status = 201)  


class full_chain(APIView):

    def get(self, request):
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return Response(response, status = 200)


class register_node(APIView):

    def post(self, request):

        nodes = request.data['nodes']

        if nodes is None:
            return Response({'message': 'Error: Please supply a valid list of nodes'}, status = 400)

        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes),
        }
        return Response(response, status = 201);


class consensus(APIView):

    def get(self, request):

        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }

        return Response(response, status = 200);




    