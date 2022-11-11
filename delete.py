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
    
    with open('output.json', 'r') as file:
        data = json.load(file)
    file.close()

    for i in data:
        SUBSCRIPTION_ID = i['Subscription ID']
        VIRTUAL_MACHINE_NAME = i['Virtual Machine Name']
        GROUP_NAME = i['Group Name']

        resource_client = ResourceManagementClient(
            credential=cred,
            subscription_id=SUBSCRIPTION_ID
        )
        
        compute_client = ComputeManagementClient(
                credential=cred,
                subscription_id=SUBSCRIPTION_ID
            )
        # Delete virtual machine
        compute_client.virtual_machines.begin_power_off(
            GROUP_NAME,
            VIRTUAL_MACHINE_NAME
        ).result()
        print("Shutting down virtual machine.\n")

        compute_client.virtual_machines.begin_delete(
            GROUP_NAME,
            VIRTUAL_MACHINE_NAME
        ).result()
        print("Deleted virtual machine.\n")

        # Delete Group
        resource_client.resource_groups.begin_delete(
            GROUP_NAME
        ).result()
        print("Deleted group.\n")

    return 
    
if __name__ == "__main__":
    main()