# Gan_Shmuel Development Week - Blue Team

## Basic Rules:
1) MAIN BRANCH = PRODUCTION!
2) every dev team should work in his own folder

		* billing in /billing
		* weight in /weight  
		* DevOps in /devOps	
2) every team should work in his own branch.
4) merging to main branch is by request, and done with a devOps team member.

## Merging into "main" = Going to Production
Merging into main will be done in the following process:
1) back-merge <your_brach> into local <main>, fixing any merging issues. 
2) push request to <main> in gitHub (origin) - with a DevOps team member only. (This will update the server)

## Architecture Rules:
1) Production Ports:
		* 8080 - Weight
		* 8081 - Billing
		* 8086 - DevOps (/Webhook)

2) Testing Ports: 
		* 5000 - Weight
		* 4000 - Billing
3) Enviroment Variables:
		*
		*
		*
