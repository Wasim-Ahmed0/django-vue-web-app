# Django-Vue webapp showcasing AJAX requests

## Create conda environment

After cloning this repository, create a conda environment for this project and activate the environment:

```console
$ conda create --name djangovue python=3.11
$ conda activate djangovue
```

## Django backend

### Install backend (Python) dependencies

With the conda environment active, install the backend (Python) dependencies:

```console
(djangovue)$ cd backend
(djangovue)$ pip install -r requirements.txt
```

The main backend dependencies (see requirements.txt) are the Django framework itself (Django) and [django-cors-headers](https://pypi.org/project/django-cors-headers/) which is needed for CORS requests (since the request origin address http://localhost:5713 is different from the address that sent the JavaScript code to the browser http://localhost:8000).

### Start backend server

To start the backend server cd into the backend folder where the manage.py file is (if not already there)

```console
(djangovue)$ cd backend
```

and run

```console
(djangovue)$ python manage.py runserver
```

The server will start on http://localhost:8000

## Vue frontend

### Install frontend (JavaScript) dependencies

To install the frontend (JavaScript) dependencies cd into the frontend folder

```console
(djangovue)$ cd frontend
```

and run:

```console
(djangovue)$ npm install
```

The main frontend dependencies (see package.json) are [vue](https://vuejs.org/guide/introduction.html) and [bootstrap](https://getbootstrap.com/docs/5.0/getting-started/download/).

### Start frontend server

To start the frontend server run

```console
(djangovue)$ npm run dev
```

and the server will start on http://localhost:5173
