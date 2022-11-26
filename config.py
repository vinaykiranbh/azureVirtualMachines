import os
from typing import Any
import json 

class Config:

    with open('config.json') as file:
        data = json.load(file)
    file.close()

    @staticmethod
    def getSubscription() -> str:
        return Config.data["subscription"]

    @staticmethod
    def getGroupName() -> str:
        return Config.data["groupname"]
    
    @staticmethod
    def getVnetName() -> str:
        return Config.data["vnet_name"]
    
    @staticmethod
    def getSubnetName() -> str:
        return Config.data["subnet_name"]
    
    @staticmethod
    def getIpName() -> str:
        return Config.data["ip_name"]

    @staticmethod
    def getIpConfigName() -> str:
        return Config.data["ip_config_name"]

    @staticmethod
    def getNicName() -> str:
        return Config.data["nic_name"]
    
    @staticmethod
    def getVnetAddress() -> list:
        return Config.data["vnet_address"]
    
    @staticmethod
    def getLocation() -> list:
        return Config.data["location"]
    
    @staticmethod
    def getSubnetAddress() -> str:
        return Config.data["subnet_address"]
    
    @staticmethod
    def getVMSize() -> str:
        return Config.data["vm_size"]
    
    @staticmethod
    def getAdminUsername() -> str:
        return Config.data["admin_username"]
    
    @staticmethod
    def getAdminPassword() -> str:
        return Config.data["admin_password"]
    
    @staticmethod
    def getVirtualMachineName() -> str:
        return Config.data["virtualMachineName"]
    
    @staticmethod
    def getNoIP() -> int:
        return Config.data["no_of_ip"]
    
    @staticmethod
    def getSecurityGroupName() -> str:
        return Config.data["SecurityGroupname"]
    
    @staticmethod
    def getinboundRuleName() -> str:
        return Config.data["inboundrulename"]
    
    @staticmethod
    def getoutboundRuleName() -> str:
        return Config.data["outboundrulename"]

    @staticmethod
    def getSSHKeyName() -> str:
        return Config.data['SSHKeyName']