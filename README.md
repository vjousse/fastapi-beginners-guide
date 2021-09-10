# fastapi-beginners-guide

## exec test with docker
1. launch the app in daemon mode `docker-compose up -d`
1. access the bash of the container `docker exec -it fastapi-beginners-guide_web_1 bash`
1. exec test `pytest --disable-warnings app/tests/views/test_home.py`