# blockchain_django

이 리포지토의 코드는 다음글을 참고하여 작성하였습니다. [원글 포스트](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

원글의 번역: [링크](https://blog.naver.com/godori91/221205018337)




### 설치

1. [python3.6](w.python.org/downloads/) 이상이 설치되어 있어야합니다.
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


