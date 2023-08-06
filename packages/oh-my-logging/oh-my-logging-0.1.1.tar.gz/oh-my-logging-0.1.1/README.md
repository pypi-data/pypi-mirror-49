# oh-my-logging
An extension for logging module.

# Install
```
pip install oh_my_logging
```

# Usage
## Decorators
### logger

Inject logger object to function as the last parameter.
```
from oh_my_logging.decorators import logger

@logger
def myprint(message, logger):
    logger.debug(message)
    logger.info(message)
    logger.warn(message)
    logger.error(message)
    
myprint('hello')
```

### log_args

Log arguments of function.
```
from oh_my_logging.decorators import log_args

@log_args
def sum(a, b):
    return a + b
    
sum(1,2) # echo 'params: a=1, b=2'
```

### log_returnings

Log retuning value of function.
```
from oh_my_logging.decorators import log_returnings

@log_returnings
def sum(a, b):
    return a + b
    
sum(1,2) # echo 'returning: 1'
```

### log_stat

Count the execution time cost of specific function.
```
from oh_my_logging.decorators import log_stat

@log_stat
def sum(a, b):
    return a + b
    
sum(1,2) # echo statistic: 1.2ms'
```

### log_error

Log exception info then raise exception again, or catch then ignore specific exceptions.
```
from oh_my_logging.decorators import log_error

# Log then raise exception again.
@log_error
def myfile(name):
    raise FileNotFoundException(name)

myfile('123')

# Log then catch then ignore FileNotFoundException.
@log_error(ignore_errors=(FileNotFoundException,))
def myfile2(name):
    raise FileNotFoundException(name)
    
myfile2('123')
```

### log

Super decorator which contains funtionalities of decorators all above. If you want to log two or more information, use this decorator instead suggested.
```
from oh_my_logging.decorators import log

@log(log.ARGS, 
     log.RETURNING, 
     log.STAT, 
     {'target': log.ERROR, 
      'ignore_errors': (FileNotFoundException,)})
def myfile(name):
    raise FileNotFoundException(name)

myfile('123')
```

## Logging Configuration
### Default Configuration
The default logging configuration stored in `$PWD/logging.ini`.

### JSON/YAML Configuration
```
from oh_my_logging.builders import LoggerBuilderFactory

# JSON
LoggerBuilderFactory('/path/to/logging.js')

LoggerBuilderFactory.unsafe_clear()
LoggerBuilderFactory('/path/to/logging.json')

# YAML
LoggerBuilderFactory.unsafe_clear()
LoggerBuilderFactory('/path/to/logging.yml)

LoggerBuilderFactory.unsafe_clear()
LoggerBuilderFactory('/path/to/logging.yaml)
```

### Dict Configuration
```
from oh_my_logging.builders import LoggerBuilderFactory

dictConfig = {
    'version': 1,
    'root': {
        'level': 'DEBUG',
        'handlers': ['memory'],
    },
    'handlers': {
        'memory': {
            'class': 'oh_my_logging.handlers.MemoryHandler',
            'formatter': 'default',
        },
    },
    'formatters': {
        'default': {
            'format': '%(message)s',
        },
    },
}
LoggerBuilderFactory(dictConfig)
```
