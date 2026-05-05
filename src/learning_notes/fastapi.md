# FastAPI

- Pydantic models are used to handle the request data (post, delete, etc.)  
- We can have path parameters, query parameters as well as request parameters in a single endpoint. FastAPI will handle it. The request parameters should have an equivalent Pydantic model.  
  - The function parameters will be recognized as follows:  
    - If the parameter is also declared in the **path**, it will be used as a path parameter.  
    - If the parameter is of a **singular type** (like `int`, `float`, `str`, `bool`, etc) it will be interpreted as a **query** parameter.  
    - If the parameter is declared to be of the type of a **Pydantic model**, it will be interpreted as a request **body**.  
- Putting constraints for a query parameter? Use Annotated \+ Query. Annotated from typing and Query from fastAPI:  
  from typing import Annotated  
    
  from fastapi import FastAPI, Query  
    
  app \= FastAPI()  
    
    
  @app.get("/items/")  
  async def read\_items(q: Annotated\[str | None, Query(max\_length=50)\] \= None):  
      results \= {"items": \[{"item\_id": "Foo"}, {"item\_id": "Bar"}\]}  
      if q:  
          results.update({"q": q})  
      return results  
    
- We have Path(), Header(), Body(), and Cookie() as well.  
- Query() takes min\_length, max\_length and pattern for arguments. Pattern is regex.  
- If you use such a thing the query can accept multiple values:  
  Annotated\[list\[str\] | None, Query()\]  
  In this case the statements inside the function will not change.  
- A request is a plain text, containing three parts:  
  - Start line(where the query parameter lays)  
  - Header  
  - Optional body(where the request body lays)

## Dependency injection:

- What is dependency? It means using an external thing as dependency inside another thing, without creating it inside the container. For example a car needs an engine. But it will not create it inside itself. Instead, it will use it from outside.  
- Dependency injection is not different than calling a function. However, the difference is about control. In a simple function calling, the programmer is in control. But in dependency injection, framework is.  
- For a dependency with context manager, you should always use yield. If you caught an exception, you should raise it. Otherwise the framework won’t know about it.  
- Also if you raise an error inside the dependency, there will be no need to raise it in the dependent. FastAPI will bypass the dependent and will raise the exception independently.  
- Remember, only one yield per dependency.  
- Middleware is a function that takes the request before the path operation, does something on it, then gives it to the path operation, then takes the response, then does something on it, then returns it. Somehow a “middle”man between the client and the path operation.  
- A yield dependency will run its exit code after middleware.  
- To create a middleware you need `@app.middleware("http")` on the top of the function.  
- Multiple middlewares will create a stack. The last one to be added will be executed first on the request path and last on the response path.

## Cross origin resource sharing:

- An origin is a combination of:  
  - Port  
  - Protocol  
  - Domain  
- Sometimes a single server has different ports for different services. Like running a frontend service and a backend service.  
- If JavaScript calls an origin which is different than the frontend, we’ll call it cross-origin resource sharing.  
- The request method for CORS is “option”. If the backend server finds the front end origin in allowed origins list, it will send back a kind of “authorization” header that will allow the front end server to complete its request.  
- By default, such behaviour is not allowed. To allow it, we have to add the origin to a white list called “allowed origins” in the backend server.  
- In fastAPI, you will import “cors” from “middlewares”, then make the allowed origins as a string, add it to the “CORSMiddleware” class, then add this as a middleware to the main fastAPI app you created.

- For path operation that uses a database, the session will be a dependency. If 2 path operations want to use the database to work for a single user, they will not make their sessions separately. Instead, the framework creates a session then gives this one to the both operations (this is not true for a scenario in which 2 users use these 2 operations since we want safety).  
- Session is what stores objects in memory and communicates with database using the engine  
- To make a single session per request, we will make a dependency with yield and inject it into the path operation function.  
- There is a blueprint for the structure of the files.

## A blue print for a fastAPI server:

.  
├── app                  \# "app" is a Python package  
│   ├── \_\_init\_\_.py      \# this file makes "app" a "Python package"  
│   ├── main.py          \# "main" module, e.g. import app.main  
│   ├── dependencies.py  \# "dependencies" module, e.g. import app.dependencies  
│   └── routers          \# "routers" is a "Python subpackage"  
│   │   ├── \_\_init\_\_.py  \# makes "routers" a "Python subpackage"  
│   │   ├── items.py     \# "items" submodule, e.g. import app.routers.items  
│   │   └── users.py     \# "users" submodule, e.g. import app.routers.users  
│   └── internal         \# "internal" is a "Python subpackage"  
│       ├── \_\_init\_\_.py  \# makes "internal" a "Python subpackage"  
│       └── admin.py     \# "admin" submodule, e.g. import app.internal.admin

### APIRouter: 

- you keep things organized; right? You will have the path operations for users separated from the other parts of the application. But it is in the same application. What to do about it?  
- APIRouter is a class. In the users (or any other module) you will instantiate it then treat this instance just like a regular app, creating path operation methods on it.  
- Some parameters:  
  - Prefix: every path operation of this APIRouter will have this prefix in its path  
  - Tags: this is for categorization. These categories will be applied to docs and swagger pages.  
  - Dependencies: the dependencies that you will use for all the path operations. You’ll add them here just like what you want to add on a path operation. For example you can make a whole group of the path operations to require authentication.  
  - Responses: a dict in which you can define what message should be returned if a particular error was raised  
- At the end, we can import these routers then “include” them in the main app using “include\_router”. **So each FastAPI application can only have a single app (instance of FastAPI class). The rest of stuff which are going to be separated in other files should always be defined using APIRouter.**  
- You can use the same router multiple times with different prefixed.  
- Routers can include other routers as well.

## Streaming data:

- The content type should be “application/jsonl” instead of “application/json”  
- The path operation function will have “yield” instead of “return”  
- AsyncIterable\[Item\] is a datatype for when you have json lines of the type Item (pydantic model) and you want them to be streamed. It’s for async functions.  
- For regular functions, we should use Iterable\[Item\].  
- Use cases of this are any type of data that can be structured as JSON

## Server sent events:

- These are broadcasted from server to client over HTTP. They are events that can be handled by the client’s EventSource API (it seems to be JScript).  
- This means that the client will keep an open connection, so each time there is a new event we get the update without asking.  
- The SSEs are small blocks of data containing field Like this:  
  data: {"name": "Plumbus", "price": 32.99}  
- It’s not for binary data. That is advanced.  
- Just like json, you will set yield instead of return. But   
  response\_class=EventSourceResponse  
  In the decorator arguments  
- To modify the other fields (the class fields, not the content. Something like `vent`, `id`, `retry`, or `comment`) of the event, you can use ServerSentEvent class instead of Item (pydantic model) in the yielded object and the type hint.  
- The data will be serialized as JSON. Don’t you want it? Use raw\_data instead of data as the ServerSentEvent object’s argument.  
- Last-Event-ID is an ID of the last event that the browser has received. If the connection drops, we can resume from where we were then.

## Background tasks:

- These are what will continue after sending the response.  
- Like sending an email (give the response, then you’ll ask the server to send it later)  
- Or like processing a file (send the “accepted, HTTP202” response, then start to process the file  
- To define the background task, you should first make the task function outside of the path operation function, then add background tasks as a parameter (no input is needed) with the type hint of BackgroundTasks class, then add the task function to the parameter instance using “add\_task” method. This method takes the task, sequence arguments and then the keywords arguments of the task function.  
- You can also define the background task argument in the dependency levels. They will be injected in the path operation.

## Metadata:

When creating the FastAPI app, you can use OpenAPI metadata as arguments. Just make them with AI if necessary.

## Static files:

You can use the class StaticFiles to mount a directory, which will have the static files inside. You should “mount” it in the app.  
The instance of “StaticFiles” will be another app

## Mounting

It is when an application, completely separated from the current one, is being handled by the main app. However the main app will not inherit the new app’s endpoints; it will just redirect the ones that have the mentioned prefix. The sub application could be a WSGI app (even a Django application):  
from fastapi import FastAPI  
from fastapi.middleware.wsgi import WSGIMiddleware

\# 1\. Import the WSGI application from your existing Django project.  
\# (Replace 'my\_django\_project' with the actual folder name where your Django settings.py lives)  
from my\_django\_project.wsgi import application as django\_app

\# 2\. Initialize the main FastAPI application  
app \= FastAPI()

\# 3\. Create your new, modern FastAPI endpoints  
@app.get("/api/v2/users")  
async def get\_fastapi\_users():  
    return {"message": "This request was handled blazingly fast by FastAPI."}

\# 4\. Mount the legacy Django application  
\# Every request that starts with "/legacy" will be wrapped in WSGI and sent to Django.  
app.mount("/legacy", WSGIMiddleware(django\_app))

 

## Testing

- For testing, install httpx on your python environment  
- Httpx is a python client, based on requests. You can use it to send requests to server.  
- Import TestClient class  
- Make an instance of the class, passing “app” to it. This will serve as your mock client.  
- Call the client HTTP methods and get the response for the unit tests  
- Testing functions are not asynchronous and their client calls are also normal calls, not awaited calls.  
- You need to add “test\_” before every file name for creating its test file, and in that file you need to add “test\_” before every class or method’s name to be tested.  
- Install pytest and run it. It will detect all the tests and execute them.

Debugging

- In the main function, call unicorn to debug:  
    
  if \_\_name\_\_ \== "\_\_main\_\_":  
      uvicorn.run(app, host="0.0.0.0", port=8000)


