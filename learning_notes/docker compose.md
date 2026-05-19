We make some commands in order to run our docker images. Each service in the docker compose image is one of these commands. First line is the name of the container. This will have attributes:

- Image: the name of the image (you can put “build” instead of “image” which will build the image then put its name there. Also if you put . after build, the compose file takes image from the directory in which it is located)  
- Ports: port bindings with the syntax host\_port:container\_port.  
- Environments: list of environment variables that we define using \-e flag in docker command  
- Depends\_on: it indicates the other images which this one should wait for them to be fully up and running

start/stop commands are used when you want the container data to persist. So the container will not be gone.  
up/down commands will remove the containers. If you don’t have volumes all the data will be gone.  
Environmental variables can be used in docker compose yaml file using ${varialbe name} syntax

Volume:  
After docker run command, you can add a \-v tag and a path to a folder that will be used as its volume. Like this:  
Docker run \-v name:path/to/a/folder

Docker compose file structure:  
Version:”3”  
Services:  
	Container\_name:  
	Image: image\_name  
	Ports:   
\- port:port  
Environment:

- Env\_variable1  
- env\_variable2

Run it using docker-compose \-f file.yaml up  
	