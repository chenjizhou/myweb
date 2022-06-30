# myweb for Technical Test

how to run:

check ``.env`` file existed with following value:

```
ENVIRONMENT=develop
```

this is used to deploy the app dynamically on different environment
ex: ENVIRONMENT=production is set for prod
for more, can use the IT automation application like SaltStack to deploy this file .env
 
then run under the file location: ``docker-compose up --build ``

it will start 4 container:
webapp, mysql, redis, smtp

all is already for test !

I created **two system** 

one is design server-client, that's user friendly to test with an interface.

second one is API endpoint

**to access server client :** 
- http://127.0.0.1:8088/

_after register, app will send a digit code, **you can find it in the console of docker**_ 

**to access API :** 
- http://127.0.0.1:8088/api_v2/register
- http://127.0.0.1:8088/api_v2/login
- http://127.0.0.1:8088/api_v2/confirm
- http://127.0.0.1:8088/api_v2/protected

_register do not need token, after login you will get a token_
use authorization : Bearer **** to call other API

test will use the .env under test directory to setup testing config: 
need to install test requirements
``pip install -r requirements-dev.txt``
``pytest ./api/test``


more information: 
1. with factory config, code can deploy on different environment 
2. create the logging format is friendly for index
3. all included in a docker-compose.yml, easy to setup
4. I used an orm, sorry for that, (I can remove orm if I could have few days more) 
5. I used Bearer, not Basic Auth.
6. I used redis to store the digit code, expired in 60 seconds
