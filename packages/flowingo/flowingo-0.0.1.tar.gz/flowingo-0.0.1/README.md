# flowingo

[![Test](https://github.com/k4black/flowingo/actions/workflows/test.yml/badge.svg)](https://github.com/k4black/flowingo/actions/workflows/test.yml)
[![Publish](https://github.com/k4black/flowingo/actions/workflows/publish.yml/badge.svg)](https://github.com/k4black/flowingo/actions/workflows/publish.yml)
[![codecov](https://img.shields.io/codecov/c/github/k4black/flowingo?token=ZX7TA177XY)](https://codecov.io/gh/k4black/flowingo)


like airflow but flowingo 


## Development 

### Create virtual environment 

Create venv and install packages 
```shell
python3 -m pip install virtualenv
python3 -m venv .venv
source .venv/bin/activate && pip install -r requirements.txt && deactivate
```

Activate environment 
```shell
source .venv/bin/activate
# ... work here ... 
deactivate
```


Install to local env and use it
```shell
python setup.py install easy_install flowingo[...]
flowingo --help
```



### Backend cli

You can run cli without installation 
```shell
python -m flowingo --help
```

Build and load to pip
`TODO`


### Backend server
Run manager celery worker
```shell
python -m flowingo manager 
```

Run manager celery worker with autoreload
```shell
watchmedo auto-restart --directory=./flowingo/ --pattern="*.py" --recursive -- python -m flowingo manager
```


### Backend api

`TODO`


### Frontend

`TODO`


## Build and publish 

```shell

```