# Basic REST service distribution / scaling

## Objectives

* Use docker-compose & swarm to orchestrate the REST service
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
* Why does increasing the number of workers over a certain amount decrease the total service capacity?
* How could the optimal number of nodes be increased?

## Refs: 

* https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/
* https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/
* https://blog.getpolymorph.com/7-tips-for-heavy-load-testing-with-apache-bench-b1127916b7b6
--------

## Walkthrough

``` bash 
# Initialize docker swarm
docker swarm init --advertise-addr 192.168.1.121

# Check the node is running ok
docker node ls

# Create the service
docker service create -p 8080:8080 --name football football-rest

# Check it's running as a service under swarm
docker service ls

# Generate some indicative benchmarks (1) ~ 1k rps
ab -c 8 -n 2000 -k -p ./post_data.json http://localhost:8080/football

# Scale the service for comparison
docker service scale football=4

# Verify new containers have been created for the newly scaled service
docker service ps football

# Recreate benchmarks (2) ~ 3.5k rps
ab -c 8 -n 2000 -k -p ./post_data.json http://localhost:8080/football

# Scale the service for comparison
docker service scale football=8

# Recreate benchmarks (3) ~ 3k rps
ab -c 8 -n 2000 -k -p ./post_data.json http://localhost:8080/football

# Stop (Delete) the service from the swarm
docker service rm football
```




