# View Logger

ViewLogger is a simple Django app Log view hits over time so that you know who enter this view and when.
 
## Installation

* Install the package
```sh
pip install ViewLogger
```
* Add Application to your project's INSTALLED_APPs
```python
INSTALLED_APPS = (
    '....',
    'ViewLogger',
    )
```    
* Add `ViewLogger.middleware.ViewLoggerMiddleware` to your Middleware classes .
```python
MIDDLEWARE_CLASSES = (
    '....',
    'ViewLogger.middleware.ViewLoggerMiddleware',
    )
```   

* Add `django.contrib.sessions.serializers.PickleSerializer` to your SESSION_SERIALIZER in setting.py .
```python
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
```   

* Run Migrations
```sh
   python manage.py migrate ViewLogger 
```

#### Notes
* To exempt urls add VIEWLOGGER_EXEMPTED_PATHS to your setting.py
```python
VIEWLOGGER_EXEMPTED_PATHS=["/worker"]
```   

* To exempt views add VIEWLOGGER_EXEMPTED_VIEWS to your setting.py
```python
VIEWLOGGER_EXEMPTED_VIEWS=["worker"]
```   

* ViewLogger by dafualt log all requests (GET and POST), add VIEWLOGGER_METHODS in your setting.py to log certain method , 
```python
VIEWLOGGER_METHODS=["POST"]
```   
