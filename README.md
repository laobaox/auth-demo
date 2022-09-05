# auth-demo

auth-demo project, with 2 entities: User, Role. support create user, delete user, etc

# enviroment
python3.7 or higher python version is required

```commandline
pip install -r requirements.txt
```

## run api service
python ./run_app.py
default serve on localhost:8000
swagger docment is avail at : localhost:8000/docs

## run tests
unit test: pytest tests/unit/
end to end test: pytest tests/e2e

## dependencies
fastapi: web framework
uvicorn: http server, combined with fastapi to provide http service
pydantic: used for api param model and response model

## unit test dependencies
pytest: unit test framework
requests: used in end to end test for request the api

## api spec
the interface complies with the restful specification
about restful: https://www.jianshu.com/p/b3bd2d4cde62

## layer architecture
