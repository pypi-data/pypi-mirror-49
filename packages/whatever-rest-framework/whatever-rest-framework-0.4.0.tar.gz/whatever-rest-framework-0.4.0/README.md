[![Build Status](https://travis-ci.org/filwaitman/whatever-rest-framework.svg?branch=master)](https://travis-ci.org/filwaitman/whatever-rest-framework)

# Whatever REST Framework

## DISCLAIMER:

This is WIP. Next steps I can think:
- Add support to framework=Django
- Add support to ORM=Django
- Review the TODOs I have left in the project 
- Create a better documentation (and document the base components)
- Create unit tests for base components


## What?

Basically this is an agnostic and thin layer to create RESTful APIs.


## Why?

Honestly because I every time I have to develop an API I tend to use Django just because of Django Rest Framework (and yes, this is my personal opinion).  
I would love to be able to create my RESTful APIs in whatever framework/technology I wanted to.


## How?

`pip install whatever-rest-framework`

There are a bunch of full working projects as examples. Please see the [tests folder](https://github.com/filwaitman/whatever-rest-framework/tree/master/tests).  
In short: you basically need to define the components you want to use (I suggest doing this in a base API class). For instance, below is all you need to get a simple flask API:

```python
from functools import partial

from wrf.api.base import BaseAPI
from wrf.framework.flask import FlaskFrameworkComponent
from wrf.orm.sqlalchemy import SQLAlchemyORMComponent
from wrf.schema.marshmallow_sqlalchemy import MarshmallowSQLAlchemySchemaComponent

from <your_stuff> import app, db, User, UserSchema

class MyBaseAPI(BaseAPI):
    orm_component_class = partial(SQLAlchemyORMComponent, session=db.session)
    schema_component_class = MarshmallowSQLAlchemySchemaComponent
    framework_component_class = FlaskFrameworkComponent

    def get_current_user(self):
        return {'name': 'Filipe'}

class UserAPI(MyBaseAPI):
    model_class = User
    schema_class = UserSchema

    def get_queryset(self):
        return User.query

@app.route('/', methods=['GET'])
def list_():
    return UserAPI(request).list()

@app.route('/', methods=['POST'])
def create():
    return UserAPI(request).create()

@app.route('/<int:pk>/', methods=['GET'])
def retrieve(pk):
    return UserAPI(request).retrieve(pk)

@app.route('/<int:pk>/', methods=['PATCH'])
def update(pk):
    return UserAPI(request).update(pk)

@app.route('/<int:pk>/', methods=['DELETE'])
def delete(pk):
    return UserAPI(request).delete(pk)
```


## Supported technologies

### Framework:
- Chalice
- Falcon
- Flask
- Pyramid


### ORM:
- Peewee
- SQLAlchemy


### Schema:
- Marshmallow
- Marshmallow-SQLAlchemy

Bear in mind that this project is made to be easily extensible, so if you need to connect something else, it's simple to do it.


## Contributing

Please [open issues](https://github.com/filwaitman/whatever-rest-framework/issues) if you see one, or [create a pull request](https://github.com/filwaitman/whatever-rest-framework/pulls) when possible.  
In case of a pull request, please consider the following:
- Respect the line length (132 characters)
- Keep the great test coverage of this project
- Run `tox` locally so you can see if everything is green (including linter and other python versions)
