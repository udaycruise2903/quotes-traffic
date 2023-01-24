## QuotesTraffic - A web application for user to post and search quotes related to ಬೆಂಗಳೂರು Traffic

![API](/screenshots/quotes_backend.png)

1. install pipenv
`sudo apt install python-pipenv`

2. initialise pipenv
`pipenv shell`

3. to install a package 
`pipenv install package`

4. to install requiremetns from pipfile
`pipenv install --dev`

4. to lock the environment before sending into prod
`pipenv lock`

5. to ignore pipenv file in prod(so that pipenv.lock file is used)
`pipenv install --ignore-pipfile` 

6. to generate requirements.txt (in /QuotesBackend/)
`pipenv requirements >> requirements.txt`

7. to build QuotesBackend from Dockerfile
`docker build -f docker/app/Dockerfile --tag quotes-backend .`

8. to run built docker image
`docker run -it -p 127.0.0.1:8000:8000/tcp quotes-backend`

9. to build a sqlite test
`docker compose build test-sqlite`

10. to run a sqlite test
`docker compose run test-sqlite`

11. to access the db inside container
`PGPASSWORD=somepassword pgcli -h localhost -U postgres thoughts`

12. to run postgresql test
`docker compose run test-postgresql`

13. to start server of quotes_service
`docker compose up server`
