# blockchain_django
> Work In Process (번역을 수정하고 있습니다.)  

## 개요  
장고와 python3를 이용한 블록체인 API 서버 구현 코드입니다.  

이 리포지토의 코드는 다음글을 참고하여 작성하였습니다. [원글 포스트](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

원글의 번역: [링크](https://blog.naver.com/godori91/221205018337)    

원글의 깃허브: [링크](https://github.com/dvf/blockchain)

## 목표
블록 체인 구현.      

원글의 설명에 따라 `blockchain`을 구현하며, `Django`로 API 서버를 만듭니다.    


**장고가 2.0 으로 버전 업** 이 되면서 많은 부분이 바뀌었는데 **장고 2.0** 이상 버전으로 만들어졌습니다.  

## 사용 버전
- Python: 3.6.0
- Django: 2.0.2    
- djangorestframework==3.7.7  

## 설치

1. [python3.6](https://www.python.org/downloads/) 이상이 설치되어 있어야합니다.
2. 가상환경 생성 및 활성화
```
$ python3 -m venv venv
$ source venv/bin/activate
```
3. requirements 설치
```
$ pip3 install -r requirements.txt
```
4. 실행   ( 개발 서버를 두개 실행하는 이유는 두개의 노드를 생성하고 테스트하기 위함입니다. )   
```
$ python3 manage.py runserver 0.0.0.0:8000
$ python3 manage.py runserver 0.0.0.0:8001
```
