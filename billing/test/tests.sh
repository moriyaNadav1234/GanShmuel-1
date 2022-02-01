#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
IP=0.0.0.0
PORT=5001

#Services
echo "==========Services=================="
#Health
result=$( curl "$IP":"$PORT"/health 2>/dev/null | grep "^BAD" )
if [ "$result" != "BAD" ]; then
    echo -e "Service: ${GREEN}UP${NC}"
else
    echo -e "Service: ${RED}DOWN${NC}"
fi

#DB
result=$( curl "$IP":"$PORT"/db_health 2>/dev/null | grep "^BAD" )
if [ "$result" != "BAD" ]; then
    echo -e "Database: ${GREEN}UP${NC}"
else
    echo -e "Database: ${RED}DOWN${NC}"
fi
echo "==========================================="

#API
echo "=============API health===================="
#When inserting we get an ID back, we use it after the tests to remove everything we inserted
result=$( curl "$IP":"$PORT"/provider -F name='MilkCart' 2>/dev/null | cut -d ":" -f2 | sed -E "s/[\s}]//g" | sed -E "s/\s//g")
provider_id="$result" #We get it from the previous test
if [ "$result" != "BAD" ]; then
    echo -e "Inserting into Provider: ${GREEN}Successful${NC}"
else
    echo -e "Inserting into Provider: ${RED}Failed${NC}"
fi

result=$( curl -X PUT "$IP":"$PORT"/provider/"$provider_id" -F name='Aliexp' 2>/dev/null | grep "^OK" )
if [ "$result" = "OK" ]; then
    echo -e "Updating Provider Name: ${GREEN}Successful${NC}"
else
    echo -e "Updating Provider Name: ${RED}Failed${NC}"
fi

result=$( curl "$IP":"$PORT"/truck -F id="141-32-444" -F provider="$provider_id" 2>/dev/null | grep "^OK" )
if [ "$result" = "OK" ]; then
    echo -e "Inserting into Trucks: ${GREEN}Successful${NC}"
else
    echo -e "Inserting into Trucks: ${RED}Failed${NC}"
fi

result=$( curl -X PUT "$IP":"$PORT"/truck/141-32-444 -F provider_id="$provider_id" 2>/dev/null | grep "^OK" )
if [ "$result" = "OK" ]; then
    echo -e "Updating Trucks Provider ID: ${GREEN}Successful${NC}"
else
    echo -e "Updating Trucks Provider ID: ${RED}Failed${NC}"
fi

#Reverting Test changes
