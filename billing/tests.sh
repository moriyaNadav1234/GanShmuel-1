#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

#Health
ak=$( curl 0.0.0.0:5001/health 2>/dev/null | grep "^OK" )
if [ "$ak" = "OK" ]; then
    echo -e "Service: ${GREEN}UP${NC}"
else
    echo -e "Service: ${RED}DOWN${NC}"
fi

#DB
ak=$( curl 0.0.0.0:5001/db_health 2>/dev/null | grep "^OK" )
if [ "$ak" = "OK" ]; then
    echo -e "Database: ${GREEN}UP${NC}"
else
    echo -e "Database: ${RED}DOWN${NC}"
fi