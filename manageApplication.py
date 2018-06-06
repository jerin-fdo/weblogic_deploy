import sys
import os
import re
import getopt


#from java.lang import System
#Python Script to manage applications in weblogic server.
#This script takes input from command line and executes it.
#It can be used to check status,stop,start,deploy,undeploy of applications in weblogic server using weblogic wlst tool.
#Author: Narasimha K Prasad

#========================
#Usage Section
#========================
def usage():

	print "Usage:"
	print "java weblogic.WLST manageApplication.py -u username -p password -a adminUrl [:] -n deploymentName -f deploymentFile -t deploymentTarget\n"
	sys.exit(2)

#========================
#Connect To Domain
#========================
def connectToDomain():

	try:
		connect(username, password, adminUrl)
			
		print 'Successfully connected to the domain\n'

	except Exception, err:
		print Exception, err
		print 'The domain is unreacheable. Please try again\n'
		exit()

#========================
#Checking Application Status Section
#========================
def appstatus(deploymentName, deploymentTarget):

	try:
		domainRuntime()
		cd('domainRuntime:/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
		currentState = cmo.getCurrentState(deploymentName, deploymentTarget)
		return currentState
	except:
		print 'Error in getting current status of ' +deploymentName+ '\n'
		exit()

#========================
#Application undeployment Section
#========================
def undeployApplication():

	try:
		print 'stopping and undeploying ..' +deploymentName+ '\n'
		stopApplication(deploymentName, targets=deploymentTarget)
		undeploy(deploymentName, targets=deploymentTarget)
	except:
		print 'Error during the stop and undeployment of ' +deploymentName+ '\n'

#========================
#Applications deployment Section
#========================
def deployApplication():

	try:
		print 'Deploying the application ' +deploymentName+ '\n'
		deploy(deploymentName,deploymentFile,targets=deploymentTarget)
		startApplication(deploymentName)
	except Exception, err:
		print Exception, err
		print 'Error during the deployment of ' +deploymentName+ '\n'
		exit()

#==============================================
#Checking Server Status
#==============================================
def _serverstatus():
    try:
        cd('domainRuntime:/ServerLifeCycleRuntimes/'+deploymentTarget);
        serverState = cmo.getState()

        if serverState == "RUNNING":
            print 'Server ' + deploymentTarget + ' is :\033[1;32m' + serverState + '\033[0m';
        elif serverState == "STARTING":
            print 'Server ' + deploymentTarget + ' is :\033[1;33m' + serverState + '\033[0m';
        elif serverState == "UNKNOWN":
            print 'Server ' + deploymentTarget + ' is :\033[1;34m' + serverState + '\033[0m';
        else:
            print 'Server ' + deploymentTarget + ' is :\033[1;31m' + serverState + '\033[0m';
        return serverState
    except:
        print 'Not able to get the' + serverState +'server status. Please try again\n';
        print 'Please check logged in user has full access to complete the requested operation on ' +deploymentTarget+ '\n';
        exit()

#==============================================
#Start Server Block
#==============================================

def _startServer():
    try:
	cd('domainRuntime:/ServerLifeCycleRuntimes/'+deploymentTarget);
	cmo.start()
       
	myStatus=_serverstatus()
       
	while myStatus != "RUNNING":
            myStatus=_serverstatus()
            java.lang.Thread.sleep(5000);
    except:
        print 'Error in getting current status of ' +deploymentTarget+ '\n';
        print 'Please check logged in user has full access to complete the start operation on ' +deploymentTarget+ '\n';
        exit()
#==============================================
#Stop Server Block
#==============================================

def _stopServer():

    try:
        cd('domainRuntime:/ServerLifeCycleRuntimes/'+deploymentTarget);
        cmo.forceShutdown();
        state=_serverstatus()
        while state != "SHUTDOWN":
            state=_serverstatus()
            java.lang.Thread.sleep(5000);
    except:
        print 'Error in getting current status of ' +deploymentTarget+ '\n';
        print 'Please check logged in user has full access to complete the stop operation on ' +deploymentTarget+ '\n';
        exit()


#========================
#Input Values Validation Section
#========================

if __name__=='__main__' or __name__== 'main':

	try:
		opts, args = getopt.getopt(sys.argv[1:], "u:p:a:n:f:t:", ["username=", "password=", "adminUrl=", "deploymentName=", "deploymentFile=", "deploymentTarget="])

	except getopt.GetoptError, err:
		print str(err)
		usage()

username=''
password=''
adminUrl=''
deploymentName=''
deploymentFile=''
deploymentTarget=''

for opt, arg in opts:
	if opt == "-u":
		username = arg
	elif opt == "-p":
		password = arg
	elif opt == "-a":
		adminUrl = arg
	elif opt == "-n":
		deploymentName = arg
	elif opt == "-f":
		deploymentFile = arg
	elif opt == "-t":
		deploymentTarget = arg

if username == "":
	print "Missing \"-u username\" parameter.\n"
	usage()
elif password == "":
	print "Missing \"-p password\" parameter.\n"
	usage()
elif adminUrl == "":
	print "Missing \"-a adminUrl\" parameter.\n"
	usage()
elif deploymentName == "":
	print "Missing \"-n deploymentName\" parameter.\n"
	usage()
elif deploymentFile == "":
	print "Missing \"-f deploymentFile\" parameter.\n"
	usage()
elif deploymentTarget == "":
	print "Missing \"-t deploymentTarget\" parameter.\n"
	usage()

#========================
#Main Control Block For Operations
#========================
def deployUndeployMain():

		domainConfig()
		appList = re.findall(deploymentName, ls('/AppDeployments'))
		if len(appList) >= 1:
    			print 'Application '+deploymentName+' Found on server '+deploymentTarget+', undeploying application..'
			print '=============================================================================='
			print 'Application Already Exists, Undeploying...'
			print '=============================================================================='
    			undeployApplication()
			print '=============================================================================='
    			print 'Redeploying Application '+deploymentName+' on'+deploymentTarget+' server...'
			print '=============================================================================='
			deployApplication()
	   	else:
			print '=============================================================================='
			print 'No application with same name...'
    			print 'Deploying Application '+deploymentName+' on '+deploymentTarget+' server...'
			print '=============================================================================='
			deployApplication()
#========================
#Execute Block
#========================
print '=============================================================================='
print 'Connecting to Admin Server...'
print '=============================================================================='
connectToDomain()
myStatus=_serverstatus()

if myStatus == "RUNNING":
	print '=============================================================================='
	print 'Starting Deployment...'
	print '=============================================================================='
	deployUndeployMain()
	print '=============================================================================='
	print 'Execution completed...'
	print '=============================================================================='
else:
	print '=============================================================================='
	print 'Server is not in RUNNING status.' + deploymentTarget
	print '=============================================================================='


disconnect()
exit()
