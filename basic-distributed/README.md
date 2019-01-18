# Basic REST service distribution / scaling

## Objectives

* Use docker-compose to orchestrate the REST service
* Enable demonstration of scaling the service up and down i.e. workers=1, workers=8, workers=2 ...
* Enable comparative performance stats to be gathered

## TODO
* Container stack overview
* Basic operations, start and stop the stack
* Scale the stack whilst running
* Test the stack and performance with different numbers of workers

## Questions
* How does this compare to running as a simple service on bare-metal?
* What are the performance, failure and scaling characteristics?
* How could these be improved if needed?

## Refs: 

* https://blog.docker.com/2016/06/docker-app-bundle/
* https://medium.com/@lherrera/poor-mans-load-balancing-with-docker-2be014983e5
* https://www.brianchristner.io/how-to-scale-a-docker-container-with-docker-compose/