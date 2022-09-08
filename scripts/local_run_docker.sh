export PYTHONPATH=$PYTHONPATH:../


source ./env/bin/activate

start_containers(){
    sudo docker run --name mongo-container -p 27017:27017 -d mongo:latest
    sudo docker run -it --name mosquitto -p 2883:1883  -p 9001:9001  -d -v $(pwd)/mosquitto:/mosquitto/  eclipse-mosquitto:latest
    docker run --name redis-container -p 6379:6379 -d redis
}

remove_containers(){
    sudo docker stop mongo-container 2> /dev/null
    sudo docker rm mongo-container 2> /dev/null
    sudo docker stop redis-container 2> /dev/null
    sudo docker rm --volumes redis-container 2> /dev/null
    docker stop  mosquitto 2> /dev/null
    docker rm --volumes  mosquitto 2> /dev/null
}

remove_containers()
start_containers()
remove_containers()
