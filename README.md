# aclabs2020
to do app using django + graphene on backend and apollo and react on frontend

frontend taken from https://github.com/haikyuu/graphql-todo-list 

## prerequisites
node installed

## setup

### Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

### Install Django and Graphene with Django support

pip install django==2.2

pip install graphene_django

### Start backend server

cd aclabs

python manage.py runserver 0:8000 --settings=aclabs.settings

python manage.py migrate --settings=aclabs.settings

### Start frontend server

cd client

npm start
