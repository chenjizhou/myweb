# myweb for Dailymotion Technical Test

how to run:

check ``.env`` file existed with following value:

```
ENVIRONMENT=develop
```

this is used to deploy the app dynamically on different environment
ex: ENVIRONMENT=production is set for prod

for more, can use the IT automation application like SaltStack to deploy this file .env
 
then run: ``docker-compose up -d --build ``

this will use code copied at docker image built, to use locally source folder

install all the requirements and start the application

also it will start two more services redis and mysql which is also used for the test

to deploy on lab: create develop or tag and push, then click on deploy from gitlab ;)
to stop, run the stop job the same way

migration db : ``docker- exec -it myweb sh``


