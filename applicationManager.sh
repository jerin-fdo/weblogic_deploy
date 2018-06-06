#!/usr/bin/ksh
##############################################################################################################
# Author : Narasimha Prasad
# This script, applicationManager.sh, is used to deploy Adapter on the weblogic server

#############INPUT PARAMETERS ################################################################################
#
# The template for running the script is as follows.
# ./applicationManager.sh <environment> <applicationName>
# 
# Please call the script with options
#
# E.g. ./applicationManager.sh DEV RETAIL
# E.g. ./applicationManager.sh DEV RTR
# E.g. ./applicationManager.sh DEV INQ
# E.g. ./applicationManager.sh DEV MHO
#
###############################################################################################################

###############################################################################################################
# Methods used in the script
###############################################################################################################
print_usage()
{
	echo "\nPlease follow the Syntax:
	./applicationManager.sh <environment> <applicationName> \n
	E.g. ./applicationManager.sh DEV RETAIL \n
	E.g. ./applicationManager.sh DEV RTR \n
	E.g. ./applicationManager.sh DEV INQ \n
	E.g. ./applicationManager.sh DEV MHO \n"
	exit 1
}

###############################################################################################################
# Main logic
###############################################################################################################
if [ $# -lt 2 ]
then
	echo "Insufficent arguments!"
	print_usage
fi

environment=$1
applicationName=$2

username=''
password=''
adminUrl=''
deploymentName=''
deploymentFile=''
deploymentTarget=''


if [ $environment != "DEV" ] && [ $environment != "IODIO" ] && [ $environment != "IT" ] && [ $environment != "ATBILL" ] && [ $environment != "ASTATO" ]
then
	echo "Wrong environment parameter passed"
	echo "Please select from the following options: DEV, IODIO, IT, ATBILL, ASTATO"
	exit 1
fi

if [ $applicationName != "RETAIL" ] && [ $applicationName != "RTR" ] && [ $applicationName != "INQ" ] && [ $applicationName != "MHO" ]
then
	echo "Wrong applicationName parameter passed"
	echo "Please select from the following options: RETAIL, RTR, INQ, MHO"
	exit 1
fi

if [ $environment == "DEV" ]
then

	if [ -f deployment_dev.config ]
	then

		. deployment_dev.config
	
		username=$devusername
		password=$devpassword
		adminUrl=$devadminUrl

		if [ $applicationName == "RETAIL" ]
		then
			deploymentName=$devretaildeploymentName
			deploymentFile=$devretaildeploymentFile
			deploymentTarget=$devretaildeploymentTarget
		
		elif [ $applicationName == "RTR" ]
		then
			deploymentName=$devrtrdeploymentName
			deploymentFile=$devrtrdeploymentFile
			deploymentTarget=$devrtrdeploymentTarget

		elif [ $applicationName == "INQ" ]
		then
			deploymentName=$devinqdeploymentName
			deploymentFile=$devinqdeploymentFile
			deploymentTarget=$devinqdeploymentTarget

		elif [ $applicationName == "MHO" ]
		then
			deploymentName=$devmhodeploymentName
			deploymentFile=$devinqdeploymentFile
			deploymentTarget=$devmhodeploymentTarget

		fi
	else
		echo "Configuration file: deployment_dev.config not found"
	fi 

fi
	

java -cp /FS/bea/bea/weblogic92/server/lib/weblogic.jar weblogic.WLST manageApplication.py -u $username -p $password -a $adminUrl -n $deploymentName -f $deploymentFile -t $deploymentTarget
