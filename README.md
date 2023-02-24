# SOFTDESK : Issue Tracking System

This is a solution for following task and technical issue for B2B clients.

This is a REST API using JWT for the login.  
It can manage a project with it's contributor along with issues and comments.  

## Installation :

Creating a virtual environment is advised :  
From your terminal :
```
$ python -m venv softdesk_env
```

From POSIX :
```
$ source softdesk_env/bin/activate
```

Or windows :
```
C:\ softdesk_env\Scripts\activate.bat
```

Clone this repo :
```
git clone git@github.com:Riazzor/SoftDesk.git
```

Install dependencies :
```
python -m pip install -r requirements.txt
```

Run migrations :
```
python manage.py migrate
```

Start the server :
```
python manage.py runserver
```


## You are ready to start testing :

http://127.0.0.1:8000/api/

### N.B. :

This is still an API. Use Postman to test it.
