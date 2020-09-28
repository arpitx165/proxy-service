# proxy-service
Request Proxy Service


This proxy service helps proxy to replay an HTTPS request to specified URL and returns back the response.


## Setup

1. Clone this repo and make sure **docker and docker-compose** are installed in machine.

2. In this repo we are using **python:3.7-alpine and redis:alpine** docker image.

3. In order to build the project need to run below command that will spin up the application and redis container.
  > cd proxy-service
  >
  > docker-compose up 


## Health Check


*  Once build is completed, will able to see below server status : 

>    Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
>

*  In order to verify containers are running use below command without quitting the docker-compose command terminal :

> docker ps

* Health Check API In order to check readiness of application, Hit below url in browser :

> http://localhost:5000/health

Sample response : 

```
{
  "health_check": [
    {
      "redis": true
    }
  ], 
  "status": "Ready"
}
```

**Note :** From above response we can determine application is ready for use as dependency check passed.


## Functionality 

* Now We are ready to use the application functionality.

* In order to trigger Https request need to use below endPoint with **POST** request type:

> http://localhost:5000/triggerRequest

**Supported Http Request Type**  :

* GET, POST, PUT, DELETE, PATCH


**Request Body :**

```
{
	"clientId": "test0001",
	"url": "https://jsonplaceholder.typicode.com/posts",
	"params": {"userId": 1},
	"headers": { "Content-type": "application/json; charset=UTF-8" },
	"httpRequestType": "GET",
	"requestBody": { },
}
```

**Note** 

* **Params** are request parameter that will be url enCoded.

**Response Body** :

```
{
    "data": {
        "reqData": {"data": "2"}
        "reqStatus": 200,
        "url": "https://jsonplaceholder.typicode.com/posts"
    },
    "status": "success"
}
```

**Note**

* In this **data** key will consist the object that will have request's response data and status code 


## API Rate Limiting Logic :

* Every request will go through **middleware** In that based on given clientId number of requests will be checked in last 1 min (sliding window)

* If number of requests are exceeding the limit than request will be blocked for that client and 429 (Too many requests) status will be sent.

* In docker-compose rate limiting can updated using env variable **TIME_INTERVAL**, **REQUEST_COUNT**.

* Every request has timeout of 5sec this is being applied in two way one is establishing connection with given url and getting response.

* Once redis container is exited, will lose the data as volume path for redis is not mentioned so its will not work as persistent storage.


## Testing :

* In order to run test make sure containers are up and running :

>  python test.py
