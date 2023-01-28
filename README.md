# web-project

Web Programming final project

## Installation

run `docker-compose up --build`

## Endpoints

### register
 
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

### Add url

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

### Get urls for user

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

### Get url detailes

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

### Get Alerts for an url

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
