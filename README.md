# View Logger

ViewLogger is a simple Django app Log view hits over time so that you know who enter this view and when.
 
## Installation

* Install the package
```sh
pip install ViewLogger
pip install unicodecsv
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
 you will find JSON file named From_(first date in ViewLogger table)_To_(last date in ViewLogger table).json file for example : From_2018-01-01_To_2018-12-01.json
 and the table is empty now and the auto_increment is reset 
 
 or run to load the data you have archived from one file 
```python
 python manage.py LoadViewLoggerArchivedData.py --file=file_name
```
or more than one file 
```python
 python manage.py LoadViewLoggerTable.py --files="file1_name,file2_name,file3_name"
```

* To search in ViewLogger archived files  
```python
 python manage.py SearchInViewLoggerArchives --done_by=mahmood --done_on=2018-12-01 
```
 with parameter available with examples :
 ```python
 --done_by=mahmood 
 --done_on=date
 --url=path/to/view
 --view_kwargs=key1=val1,key2=val2,
 --view_args=arg1=val1,arg2=val2,
 --view_name=view_name
 --request_body=key1=val1,key2=val2,
 --request_method=GET
 ```
 the output will generate json object with the values for example :
```json
 File =  From_2018-01-01_To_2018-12-01.json
{
  "view_args": [],
  "view_kwargs": {
    "testid": "40478"
  },
  "request_body": {
    "requestby": "mahmood",
    "resultcode": "1"
  },
  "url": "/path/to/view",
  "done_on": "2018-12-01 12:12:12.142001",
  "view_name": "Edit",
  "done_by": "mahmood",
  "request_method": "POST",
  "id": 498
}
```
 and you can save the putput in file for example : 
```python
 python manage.py SearchInViewLoggerArchives --done_by=mahmood --done_on=2018-12-01 > /path/to/output.json
```