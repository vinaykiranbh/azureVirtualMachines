try:
    import os
    import sys
    import json
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.network import models as network_models
    from config import Config
except ModuleNotFoundError:
    os.system("pip install -r requirements.txt")  # type: ignore


def main():
    
    if (os.getenv('run_locally')):
        cred = InteractiveBrowserCredential()
    else:
        cred = DefaultAzureCredential()

    SUBSCRIPTION_ID = Config.getSubscription()
    
    location = Config.getLocation()
    NIsIP = Config.getNoIP()
    
    resource_client = ResourceManagementClient(
        credential=cred,
        subscription_id=SUBSCRIPTION_ID
    )

    
    res = []
    for loc in location:
        GROUP_NAME = loc
        result_check = resource_client.resource_groups.check_existence(
        GROUP_NAME
        )
        VM_NAME = Config.getVirtualMachineName() + loc
        NSG_NAME = Config.getSecurityGroupName() + loc
        NSG_INBOUND_RULE_NAME = Config.getinboundRuleName() + loc
        NSG_OUTBOUND_RULE_NAME = Config.getoutboundRuleName() + loc
        # Step 1: Provision a resource group
        # Create resource group
        if result_check != True:
            resource_client.resource_groups.create_or_update(
                resource_group_name=GROUP_NAME,
                parameters={"location": loc}  # type: ignore
            )

        # Step 2: provision a virtual network

        network_client = NetworkManagementClient(
            credential=cred,
            subscription_id=SUBSCRIPTION_ID
        )

        VNET_NAME = Config.getVnetName() + loc
        SUBNET_NAME = Config.getSubnetName() + loc
        IP_NAME = Config.getIpName() + loc
        IP_CONFIG_NAME = Config.getIpConfigName() + loc
        NIC_NAME = Config.getNicName() + loc

        vnet_result = network_client.virtual_networks.begin_create_or_update(resource_group_name=GROUP_NAME,
                                                                            virtual_network_name=VNET_NAME,
                                                                            parameters={
                                                                                "location": loc,
                                                                                "address_space": {
                                                                                    "address_prefixes": Config.getVnetAddress()
                                                                                }
                                                                            }  # type: ignore
                                                                            ).result()

        # type: ignore
        print(
            f"Provisioned virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}")

        # Step 3: Provision the subnet and wait for completion
        subnet_result = network_client.subnets.begin_create_or_update(
            resource_group_name=GROUP_NAME,
            virtual_network_name=VNET_NAME,
            subnet_name=SUBNET_NAME,
            subnet_parameters={
                "address_prefix": Config.getSubnetAddress()}  # type: ignore
        ).result()

        print(
            f"Provisioned virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}")

        # Step 4: Provision an IP address and wait for completion
        ipAddress = []
        ip_add = []
        for i in range(0, NIsIP):
            ip_address_result = network_client.public_ip_addresses.begin_create_or_update(
                resource_group_name=GROUP_NAME,
                public_ip_address_name=IP_NAME + f"{i}",
                parameters={
                    "location": loc,
                    "sku": {"name": "Standard"},
                    "public_ip_allocation_method": "Static",
                    "public_ip_address_version": "IPV4"
                }  # type: ignore
            ).result()

            print(
                f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")
            ip_add.append(ip_address_result.id)
            ipAddress.append(ip_address_result.ip_address)

        ip_config = []
        for j in range(0, len(ip_add)):
            if j == 0:
                ipcon = {
                    "name": IP_CONFIG_NAME + f"{j}",
                    "subnet": {"id": subnet_result.id},
                    "public_ip_address": {"id": ip_add[j]},
                    "primary": True
                }
            else:
                ipcon = {
                    "name": IP_CONFIG_NAME + f"{j}",
                    "subnet": {"id": subnet_result.id},
                    "public_ip_address": {"id": ip_add[j]}
                }
            ip_config.append(ipcon)

        # Step 5: Provision the network interface client
        # Create Network Security Group
        nsg_parameters = network_models.NetworkSecurityGroup(location=loc)
        network_security_group = network_client.network_security_groups.begin_create_or_update(
            GROUP_NAME,
            NSG_NAME,
            parameters=nsg_parameters
        ).result()
        print("Create Network Security Group:{}".format(network_security_group.name))

        # Create Network Security Group Rule
        nsg_rule_parameters = network_models.SecurityRule(
            protocol='*',
            direction='inbound',
            source_address_prefix='*',
            source_port_range='*',
            destination_address_prefix='*',
            destination_port_range='*',
            access='allow',
            priority=200
        )
        nsg_rule_parameters1 = network_models.SecurityRule(
            protocol='*',
            direction='outbound',
            source_address_prefix='*',
            source_port_range='*',
            destination_address_prefix='*',
            destination_port_range='*',
            access='allow',
            priority=200
        )
        nsg_rule = network_client.security_rules.begin_create_or_update(
            GROUP_NAME,
            NSG_NAME,
            NSG_INBOUND_RULE_NAME,
            nsg_rule_parameters
        ).result()
    

        nsg_rule1 = network_client.security_rules.begin_create_or_update(
            GROUP_NAME,
            NSG_NAME,
            NSG_OUTBOUND_RULE_NAME,
            nsg_rule_parameters1
        ).result()
        

        nic_result = network_client.network_interfaces.begin_create_or_update(
            resource_group_name=GROUP_NAME,
            network_interface_name=NIC_NAME,
            parameters={
                "location": loc,
                "ip_configurations": ip_config,
                "network_security_group": { "id": network_security_group.id }
            }  # type: ignore
        ).result()

        print(f"Provisioned network interface client {nic_result.name}")

        # Step 6: Provision the virtual machine

        # Obtain the management object for virtual machines
        compute_client = ComputeManagementClient(
            credential=cred,
            subscription_id=SUBSCRIPTION_ID
        )

        USERNAME = Config.getAdminUsername()
        PASSWORD = Config.getAdminPassword()

        print(
            f"Provisioning virtual machine {VM_NAME}; this operation might take a few minutes.")

        # Provision the VM specifying only minimal arguments, which defaults to an Ubuntu 18.04 VM
        # on a Standard DS1 v2 plan with a public IP address and a default virtual network/subnet.

        vm_result = compute_client.virtual_machines.begin_create_or_update(
            resource_group_name=GROUP_NAME,
            vm_name=VM_NAME,
            parameters={
                "location": loc,
                "storage_profile": {
                    "image_reference": {
                        "publisher": 'OpenLogic',
                        "offer": "CentOS",
                        "sku": "7.5",
                        "version": "latest"
                    }
                },
                "hardware_profile": {
                    "vm_size": Config.getVMSize()
                },
                "os_profile": {
                    "computer_name": VM_NAME,
                    "admin_username": USERNAME,
                    "admin_password": PASSWORD
                },
                "network_profile": {
                    "network_interfaces": [{
                        "id": nic_result.id,
                        "properties": {
                                    "primary": True
                                }
                    }]
                }
            }  # type: ignore
        ).result()

        print(f"Provisioned virtual machine {vm_result.name}")

        result = {"Primary IP": ipAddress[0], "Secondary IP": ipAddress[1:],
                "Virtual Machine Name": VM_NAME, "Group Name": GROUP_NAME, "Subscription ID": SUBSCRIPTION_ID}
        res.append(result)
    
    with open("output.json", "w") as outfile:
        json.dump(res, outfile)
    outfile.close()
    return res

if __name__ == "__main__":
    main()
