# Microservice

-   Language: Python3
-   Framework: Falcon
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
    - falcon
    - spectree
    -  mongoengine
    -	gunicorn
    -	uWSGI

**run Server**
```
$ gunicorn config - -bind = 0.0.0.0: 8001
```


3. Status services
    /health
