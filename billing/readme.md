to run the services follow these steps(These steps are temporary until we make the services docker images):

First run the init_BillingService.sh file
```sh
./init_BillingService.sh
```

Once the script finished initalizing you have to go inside the mysql image with
```sh
docker exec -it billingDB /bin/bash
```

Then you log into the database with the command
```sh
mysql -u root -p
```

Once you are promoted to enter the password, enter catty.

Then when inside of the mysql IT,run the following command to create our billingDB
```sh
source db/billingdb.sql
```

That's it! Exit using 'exit' and then 'exit' again to get out of the container.

Then we have to go to the api service container using the command
```sh
docker exec -it apiService sh
```
once inside go to the billing directory
```sh
cd billing
```

Inside of there you'll find a script named run_api.sh
```sh
./run_api.sh
```

Once this script is ran it'll download all that's required to run the service with the db and you can start using the api like so
```sh
cur 0.0.0.0:5001/provider -F name="Mike"
```
Some of the apis are still not working very well. Those bugs will be fixed by us as a team :)
# sharef is Number1