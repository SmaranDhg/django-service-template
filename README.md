# Project Setup Instructions

### Using docker
```bash
docker compose build
docker compose up 
```


# Assumptions

- Docker is installed on the host machine.
- Code will be run with `env/.local.properties` as default and other configs are for showing the modularity and scalabilty in future rather than a current functional requirement.
- Two apps discussed will potentially be broken down into two separate services in future.
- Regarding data model, same for patient: `user,patient's full_name` should be unique, for assessment `patient, assessment's name` should be unique. 



# Challenges

- Whether to have dependency coupling between assessment_management and patient_management,
as the data_layer shares the foreign key relation.
This really made me think whether to put the models in same app. But decided to move forward to tolerate the coupling for now, which latter can be broken down to uuid relation instead of ForeighKey,if they were to be microservices later.


# Additional Feature or improvements
- Well idk its additional feature or not, but I have added serializers to have the `type information` as `__typename` which comes handy in future debugging and enhancement.
- Also, added the utility code as `Renderer` class for `automatic formating of the API response`
- Added the `ordering searching filtering and pagination` using `django backends`
- Added the `multi tenancy` with `same database different schema model`, where per request tenant selection is based on the `auth_user` rather than the `subdomain`.

# Deployment in AWS
- Well deployment in aws can go to multiple routes here, depending on our need. But it can boil down between two, whether the app will be developed as monolith or a microservice (i.e architectural decision).

- ##### Monolith route
    - We can deploy it to a self managed EC2 instance with setting like volumns (EBS) setup manually, in this case just 
        - Running the docker container as `docker compose up`, inside the instance.
        - Exposing the domain to EC2's public ip or `assigned elastic IP`, using `route 53`.
        - Also you can setup `nginx as reverse proxy` to your interal port (optional). But good to have.
    - Using managed service like `Elastic BeanStalk`. Which gives `monitoring with CloudWatch`, `loadbalancer` and `autoscaling` making it easy
        - Setup aws cli and go through `EB Environment and Application` setup.
        - Point your domain to `EB application DNS` using `route 53`
        - Optionaly you can setup `CodePipeLine` to directly deploy to `EB application` for `CI\CD`
- ##### Microservice route
    - Here there is two possible route that `Elastic Container Service(ECS)` or `Elastic Kubernetes Service(EKS)`, base on expertise and need, _(Also `serverless with lambda` but as we are using docker and writing our own server with django so whats the point.)_ But EKS application need more specialized expertise which I dont have. But ECS is just as good and more simpler.

        - ###### ECS
            - Just contianarize the service with docker and push to container registery either `docker hub` or `elastic container registry`.
            - Create `task defination` similar to `docker compose` for defining a `task` _(aka microservice app)_
            - Expose these services using `API Gateway` and make communication, auth and ratelimiting in the `API Gateway` settings.   
- So these are the high level overview of possible deployment strategies we can go through using AWS for this app. Note all above options I have personally explored, excepts `EKS` which I have purely theoritical understanding of, so I ommited discussion of it.