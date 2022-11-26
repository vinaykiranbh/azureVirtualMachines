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


if (os.getenv('run_locally')):
        cred = InteractiveBrowserCredential()
else:
    cred = DefaultAzureCredential()

SUBSCRIPTION_ID = Config.getSubscription()

network_client = NetworkManagementClient(
            credential=cred,
            subscription_id=SUBSCRIPTION_ID
        )

network_interface = network_client.network_interfaces.get(
        "eastus",
        "/subscriptions/2b7193da-94e4-49e9-bca9-600dcbc8ccff/resourceGroups/eastus/providers/Microsoft.Network/networkInterfaces/test_network_interfaceeastus"
    )

