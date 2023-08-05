# py_spring_config

**Purpose**

Module for custom Dynaconf loader to access a Spring Config server using Github config store

**Use**

Requires the following environment variables to be set:
CONFIG_SERVER
APP_NAME
PROFILE

The loader substitutes underscores for dots in the key names retrieved from the Spring Config server, rather than preserving the nested configuration structure.
Use the loader with a Dynaconf LazySettings instance:
```
LazySettings(LOADERS_FOR_DYNACONF=['py_spring_config.loader', ...])
```

py_spring_config.config contains an example wrapper function.
```config.load_config(environment)``` assumes you have a settings.toml file in the root of the Python project, and loads either a 'local' or 'production' config.


**Example**

github.com/myorg/configrepo/myapp/config.yaml
```
---
myapp:
  django:
    secret_key: 123
```
settings.py
```
from py_spring_config.config import load_config

DEBUG = os.getenv('DEBUG', "").upper()=="TRUE"
dynaconf_settings = load_config('production') if not DEBUG else load_config('local')
SECRET_KEY = dynaconf_settings.get('myapp_django_secret_key')

```

**Running Tests**

```
python -m unittest discover -s 'tests' -p 'tests.py'
```