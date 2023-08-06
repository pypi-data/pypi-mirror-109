# Microservice

-   Language: Python3
-   Framework: FastApi
-   Database: MongoDB
-   Container: Docker

#
# Instalation

1.  Install Virtualenv and activate it

```
virtualenv - p python3 venv
```

```
source venv/bin/activate
```

2.  Install requirements.txt

```
pip3 install - r requirements.txt
```
-   Libraries:
    - fastApi
    - spectree
    - mongoengine

**run Server**
```
$ uvicorn config.settings:app --host=localhost --port=8001 --reload --log-level=inf
```


3. Status services
    /health
