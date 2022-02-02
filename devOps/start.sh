#! /bin/bash
echo "#########################"
echo "## deleting containers ##"
echo "#########################"
docker container rm -f $(docker container ps -a -q)
docker rmi -f billing_testbilling_img

docker-compose build
echo "#########################"
echo "## deleting containers ##"
echo "#########################"

# echo "q to quit, any key to continue"
# read -r -n 1 key
# if [[ $key == q ]]
# then 
#     print"\nQuitting"
#     exit
# fi

docker-compose up # > dc-up.log
echo "########################"
echo "## entering container ##"
echo "########################"

docker exec -it ci_server bash