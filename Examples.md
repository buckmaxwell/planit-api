# PlanIt: API


## Authentication

For all endpoints with the exception of POST /users (to create a new user) authentication is required.  To Authenticate simply set 'Authorization' in your request header to your user id.  It should look something like this.

```http
Authorization: Jacob-Bettencourt-Glatt63
```

Our auth is super simple, and is primarily meant to make sure users only perform actions they are allowed to perform.  One current security issue is that if the name of a user with elevated privilges were leaked, some damage could be done.  This issue will be addressed in the future, but in the meantime, lets keep this in mind ;)



## Creating a user


### POST /users
Create an administrative user.

request data:
```json
{
   "data": {
      "type": "users",
      "attributes": {
         "role": "ADMIN_ROLE"
      }
   }
}
```

create a regular user.

```json
{
"data": {"type": "users", "attributes":{"role": "USER_ROLE"}}
}
```

### POST /categories

*Only administrators can create categories*

```json
{
   "data": {
      "type": "categories",
      "attributes": {
          "id": "Arts"
      }
   }
}
```



### POST /events

*Only event creators and administrators can post events*

```json
{
   "data": {
      "type": "events",
      "attributes": {
         "title": "Fun Fake Event 1",
         "description": "This fake event is sure to make you have fake fun",
         "start_time": "2015-11-7 16:30:00",
         "end_time":  "2015-11-7 18:30:00",
         "location": "Location: Sheraton Columbus on Capitol Square",
         "address": "75 E. State St. Columbus, OH 43215",
         "lon": 39.959746,
         "lat": -82.997825,
      },
      "relationships": {
         "categories": {
            "data":[
               {"id": "Arts", "type":"categories"}
            ]
         }
      }
   }
}
```

### POST users/\<id>/relationships/events

```json
{
  "data": [
    {
      "type": "events",
      "id": "d2b7508d-4030-4397-b860-4adf34694f19",
    }
  ]
}
```
