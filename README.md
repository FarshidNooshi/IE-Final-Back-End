<div align="center">
	<h1>In The Name Of GOD</h1>
</div>

# Web Project - Internet Engineering Final Backend Project

This project is a web programming final project for Internet Engineering course at Amirkabir University of Technology. The project is built using Django, a high-level Python web framework, and provides a RESTful API to handle user registration, login, and URL monitoring functionality.

The project provides endpoints for users to register, login, add URLs for monitoring, retrieve URLs for their account, retrieve details for a specific URL, and retrieve alerts for a specific URL.

By using this project, users can monitor the status of their desired websites and receive alerts if the website experiences more than a certain number of errors. This can help users ensure the availability of their websites and take timely action if there are any issues.

## Introduction

This project was created as a final project for Internet Engineering course at Amirkabir University of Technology. It is a simple RESTful API that enables users to manage urls and monitor their availability.

## Installation

To run the project, you need to have [Docker](https://www.docker.com/) installed.

1. Clone the repository

``` terminal
$ git clone https://github.com/FarshidNooshi/IE-Final-Back-End.git
```
2. Navigate to the project directory

``` terminal
$ cd IE-Final-Back-End
```

3. Build and run the project using docker-compose

``` terminal
$ docker-compose up --build
```


## Endpoints

The following endpoints are available in the backend:

### Register

The register endpoint allows you to create a new user account.
 
``` json
{
   "name": "register",
   "url": "http://localhost:8000/api/register/",
   "method": "POST",
   "body": {
    "type": "json",
    "raw": {
        "first_name": "Farshid",
        "last_name": "Nooshi",
        "password": "a",
        "email": "farshidnooshi7262@a.com",
        "username": "something"
    }
   }
}
```

### Login

The login endpoint allows you to log in with an existing user account.

``` json
{
 "name": "login",
 "url": "http://localhost:8000/api/login/",
 "method": "POST",
 "body": {
  "type": "json",
  "raw": {
    "username": "first_user_name",
    "password": "a"
  }
 }
}
```

### Add URL

The add URL endpoint allows you to add a new URL to be monitored by the backend.

``` json
{
 "name": "add url",
 "url": "http://localhost:8000/api/webpage/",
 "method": "PUT",
 "body": {
  "type": "json",
  "raw": {
	"url": "https://www.goo12323135sfdggle.com/",
	"max_error": "2"
  }
 },
 "auth": {
  "type": "bearer",
  "bearer": "your token"
 }
}
```


### Get URLs for User

The get URLs for user endpoint returns the list of URLs associated with the user account.

``` json
  {
   "name": "profile",
   "url": "http://localhost:8000/api/profile/",
   "method": "GET",
   "auth": {
    "type": "bearer",
    "bearer": "your token"
   }
  }
```


### Get URL Details

The get URL details endpoint returns details about a specific URL.

``` json
{
 "name": "get url",
 "url": "http://localhost:8000/api/webpage?webpage_url={{url}}",
 "method": "GET",
 "auth": {
  "type": "bearer",
  "bearer": "your token"
 }
}
```


### Get Alerts for an URL

The get alerts for an URL endpoint returns a list of alerts generated for a specific URL.


``` json
  {
   "name": "get alerts",
   "url": "http://localhost:8000/api/alarm?webpage_url={{url_id}}",
   "method": "GET",
   "auth": {
    "type": "bearer",
    "bearer": "your token"
   }
  }
```
