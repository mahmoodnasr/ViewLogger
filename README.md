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

* Run Migrations
```sh
   python manage.py migrate ViewLogger 
```

#### Notes
* To exempt urls add VIEWLOGGER_EXEMPTED_PATHS to your setting.py
```python
VIEWLOGGER_EXEMPTED_PATHS=["/worker",]
```   

* To exempt views add VIEWLOGGER_EXEMPTED_VIEWS to your setting.py
```python
VIEWLOGGER_EXEMPTED_VIEWS=["worker",]
```   

* To exempt parameters add VIEWLOGGER_EXEMPTED_PARAMETER to your setting.py
```python
VIEWLOGGER_EXEMPTED_PARAMETER=["password",]
```   

* ViewLogger by dafualt log all requests (GET and POST), add VIEWLOGGER_METHODS in your setting.py to log certain method , 
```python
VIEWLOGGER_METHODS=["POST"]
```   

* To archive/load ViewLogger_Log table add VIEWLOGGER_ARCHIVE_DIR to your setting.py
```python
VIEWLOGGER_ARCHIVE_DIR = os.path.join(BASE_DIR, "ViewLoggerArchive")
```   
Then run to archive data 
```python
 python manage.py ArchiveViewLoggerTable
```  
 you will find JSON file named From (first date in ViewLogger table) To (last date in ViewLogger table).json file for example : From 2018-01-01 To 2018-12-01.json
 and the table is empty now 
 
 or run to load the data you have archived from one file 
```python
 python manage.py LoadViewLoggerArchivedData.py --file=file_name
``` 
or more than one file 
```python
 python manage.py LoadViewLoggerArchivedData.py --files="file1_name,file2_name,file3_name"
``` 