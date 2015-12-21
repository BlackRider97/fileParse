Installation on Ubuntu:
=======================
1. $sudo apt-get install fabric              (install fabric )
2. $sudo apt-get install python-virtualenv   (installl virtaualenv)
3. $sudo apt-get install python-dev libmysqlclient-dev python-mysqldb (install mysql and its python client dependencies)
4. $sudo apt-get install -y redis-server (install redis)
5. $redis-server ( to run the redis server )
6. Make sure mysql is running


How to run server:
=================

$ cd /path-to-this-directory/file-parse/  ( go to this project directory)

On localhost
-------------
Bootstrap the project ( only one time requirement )
1. fab setup_localhost

To run the server
1. source ./venv/bin/activate 
2. python fileparse/server.py 

Also added fabfile for production and staging environment which uses supervisor as process watcher.
see supervisor conf file
$ vi ./bin/fileparse.conf 


On production
-------------
Bootstrap the project ( only one time requirement )
1. fab production create_virtualenv

To depoy code and run the server
1. fab production all


On staging
-------------
Bootstrap the project ( only one time requirement )
1. fab staging create_virtualenv

To depoy code and run the server
1. fab staging all  

Also added fabfile for production and staging environment which uses supervisor as process watcher.
see supervisor conf file
$ vi ./conf/fileparse.conf

 
Uses:
=====
1. curl localhost:5000/get_logs/1450708114/le/hikesecretsanta -X GET
{
  "data": [
    {
      "cts": 1450703522802, 
      "dev_id": "and:c8eadd87411711efee1141193465694fb3130e42", 
      "distinct_id": "VNCIN-V-i3ewp-6U", 
      "et": "nonUiEvent", 
      "fr": "+919999683956", 
      "i": "1450703522", 
      "md": {
        "app_version": "3.9.9.82", 
        "bot_msisdn": "+hikesecretsanta+", 
        "bot_name": "Secret Santa", 
        "ek": "cbot_m", 
        "networkType": "1", 
        "platformUid": "VSuVLCcDwWTxhIbb"
      }, 
      "sid": "1450703519477", 
      "st": "dwnld", 
      "tag": "mob", 
      "ts": 1450703523
    }
  ], 
  "status": "ok"
}

