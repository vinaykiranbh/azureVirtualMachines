Please do only chnages in Config.json file


1. add subscription id for deployment and credentials


2. add ur desired location to deploy virtual machine

"location": "eastus"


3. add group name

if already present, it will use the existing group name or else it will create the group mentioned in config.json 


4. please do rename all of the below parameters for every location without spaces.

"vnet_name": "testVnetname",
"subnet_name": "testsubnet",
"ip_name": "testIpAddress",
"ip_config_name": "test_ip_config",
"nic_name": "test_network_interface",

5. "vnet_address": ["10.0.0.0/16"],
    "subnet_address": "10.0.0.0/24",

please do change the ip prefixes for every location

6. "vm_size": "Standard_DS1_v2",

add your desired vm size 

7. for admin

"admin_username": "azureuser",
"admin_password": "ChangePa$$w0rd24",

please do add your admin user name and password 

password should be strong with letters,numbers and symbols with 8 min character

8. "virtualMachineName": "testMachine",

please do rename without spaces - for your virtual machine 

9. add no of ip address required for your each virtual machine 

10. if u want to change the os and version - change from line 201-204 of main.py file


NOTE: please make sure there are no spaces and wait for atleast 180 sec for deployment after each run. for better understanding please wait for atleast 5 mins between each run of this python file. 

