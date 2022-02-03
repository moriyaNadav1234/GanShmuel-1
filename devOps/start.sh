#! /bin/bash
echo "#########################"
echo "##  DC Down CI Server  ##"
echo "#########################"
echo ""
docker-compose down
echo ""
echo "#########################"
echo "## deleting containers ##"
echo "#########################"
echo ""
docker container rm -f $(docker container ps -a -q)
echo ""
echo "#########################"
echo "##       DC Build      ##"
echo "#########################"
echo ""
docker-compose build

# echo "q to quit, any key to continue"
# read -r -n 1 key
# if [[ $key == q ]]
# then 
#     print"\nQuitting"
#     exit
# fi
echo ""
echo "########################"
echo "##       DC UP        ##"
echo "########################"
echo ""
docker-compose up # > dc-up.log


docker exec -it ci_server bash