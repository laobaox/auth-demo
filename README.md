#intro 
auth-demo project, with 2 entities: User, Role. support create user, delete user, etc
python version: 3.7 or higher

# run in commandline

prepare python env

```
virtualenv -p python3 venv
source venv/bin/activate
```

install dep
```
pip install -r requirements.txt
```
run app
```
python run_app.py
```

run test
```
pytest tests/unit
pytest tests/e2e
```

# run in pycharm
run run_app.py after prepare the enviroment


## Dependencies
* fastapi - web framework
* uvicorn - http server, combined with fastapi to provide http service
* pydantic - used for api param model and response model
* pytest - unit test framework
* requests - used in end to end test for request the api

## api spec
the interface complies with the restful specification
about restful: https://www.jianshu.com/p/b3bd2d4cde62

## layer architecture
from high to low
* api service: ./auth_demo/app.py
* service layer: ./auth_demo/service_layer/
* domain layer: ./auth_demo/doamin
* repository: ./auth_demo/adapters/repository.py
