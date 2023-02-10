# D1g1t django happiness API exercise

Stack: python3, django and rest_framework

## Assumptions

- Team members (users) only belong to one team at a time
- Teams might need to be removed, users moved around teams
- Timezone considerations can be ignored
- Happiness level is input as an integer between 1 and 5, inclusive

## Technical considerations

### HTTPS requirement

I used REST framework's standard `TokenAuthentication` for auth. With private tokens being passed in the request headers, we would have to make sure that the HTTPS protocol is used so that this token handshake is encrypted.

This being an exercise, I made sure to add multi-environment support, modularizing code to a dev environment, where I'm using the standard Django `manage.py runserver` over http for local development.

If this went beyond an exercise to a live/production setting, we'd create prod env configuration files for docker and django, with a webserver like nginx (which can force HTTPS) and a web service gateway interface like uWSGI.

### Custom user object

I didn't want to use the User or Group models Django provides for a few reasons:

- Django allows for many to many relationships between its Users and Groups
- Team members only belong to one team
- Team model would likely need to support new requirements in the future
- It's actually recommended to build your own custom user model

### Usage of function and class-based views

For model backed views like Happiness, the ModelViewSet offers a clean generic that can be easily overridden.

The requirements called for the Stats view to be more flexible, supporting unauthenticated requests also, so I chose a function-based view for this endpoint.

## Documentation

### Requirements

You'll need to install Docker Desktop on your machine (https://www.docker.com/products/docker-desktop/)

### Building local development environment

Containers can be built and launched from a terminal prompt at the root of the codebase:
```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

A code analysis is run using pylint during the container build.

The backend container runs a wait-for-it entrypoint so that it starts after the DB container is up and running.

After the DB is available, the Backend:
- Makes and executes DB migrations
- Runs the unit and integration tests
- Starts the development webserver

### Creating local Admin user

Now that your stack is running locally, create an Admin user:

Get a list of running containers:
```
docker ps
```

Get the container ID for the backend, and run:
```
docker exec -it <BACKEND_CONTAINER_ID> python /backend/manage.py createsuperuser --noinput
```

Now you can visit http://localhost:8000/admin/ and sign in with:
- username: admin
- password: pass

### Creating a Team and Team Member (user)

1) Sign into Admin
2) Add a Team
3) Add a TeamMember, adding them to the team in the process

### API tokens

In order to make API calls, get an API token for your user by POSTing a json with username and password properties to `/api-token-auth`

For example, using the admin user you created above:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"admin","password":"pass"}' \
  http://localhost:8000/api-token-auth/
```

To invalidate the token, DELETE `/token`:
```
curl --request DELETE \
  --header "Authorization: Token <TOKEN>" \
  http://localhost:8000/token/
```

### Using the API:

Now that you have an API token for your user, you can use it as a header in requests where auth is necessary.

Submit a happiness report as a user: (replace token and rating values)
```
curl --header "Content-Type: application/json" \
  --header "Authorization: Token <TOKEN>" \
  --request POST \
  --data '{"rating":<RATING>}' \
  http://localhost:8000/happiness/
```

Viewing stats as a user: (replace token value)
```
curl --header "Authorization: Token <TOKEN>" \
  http://localhost:8000/stats/
```

Viewing stats anonymously:
```
curl http://localhost:8000/stats/
```
