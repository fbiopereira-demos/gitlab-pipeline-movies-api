# Movies API (Gitlab CI demo)

### Description

This API was created to demonstrate an Gitlab CI pipeline that build an application docker image (deployed to docker hub) and deploys it to two kubernetes environments based on the git brahch.
I haven't use any code best practices do develop this API. The focus was the pipeline.

### Running API locally

Please use docker-compose.yaml to run this app in your local environment.
Go to http://localhost/docs to check API endpoints.

## Running API test

You will need a python environment and a local mongo db to run the tests. Also, you must configure the followings environment variables:
- SERVICE_NAME = "movies-api"
- ENVIRONMENT = "development"
- MONGO_URI = mongodb://localhost:27017/movies
- LOG_PATH = ./log/

Then install requirements in your environment and run de command behave


## Explaining the pipeline

- Behave tests will run in any branch except TAGS

  
- Deploy to docker hum will run on Master and TAGs branches
    * The image will be delivered to docker hub
    * Please pay attention that docker hub variables must be created in GitLab Ci/CD interface

    
- Deploy to kubernetes
    * In this scenario I am deploying apps to a K8s hosted at Digital Ocean
    * It is the same cluster, but master branch goes to a namespace and tag to another one
    * Again Digital Ocean credentials must be configured in Gitlab Ci/CD variables interface
    

- Gitlab still user master as default branch name. I haven't change it to Main, but fell free to do this change by yourself    
    
