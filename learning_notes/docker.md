How to debug it:

- “docker logs” is a command that shows you the logs of the container.  
- “docker exec” will give you the terminal of the running docker.  
- “docker build” makes the image

Dockerfile:

- Blueprint for making the docker image

Syntax:  
FROM \<image name from the docker hub\>  
ENV \<environemtn variable name\>=\<the value\>  
RUN \<any linux command, will be run on the container machine and not on the local machine\>  
COPY \<source from the host\> \<dest on the container machine\>  
CMD \[\<part one of the command\>, \<part two of the command\>, …\]

- Only one CMD could be here, and it is the entry point for the container machine. You can’t use RUN instead.  
- You can have multiple RUN commands, but you should keep them minimum.  
- CMD will be used as default when you are running the docker image by docker run, if you don’t specify another command.  
- COPY have access to the host machine; RUN doesn’t.  
- Each image is based on another image (the one you summon using FROM). This means it is adding a new layer to the previous one that was summoned. And the one before that, has already used another imaged so we have a hierarchy of images.

