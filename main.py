import os
import yaml
from ansible.module_utils.basic import AnsibleModule
from ansible.runner import Runner
from ansible.inventory import Inventory

def run_module():
    # Define the module's argument spec
    module_args = dict(
        router_config=dict(type='str', required=True),
        switch_config=dict(type='str', required=True),
        vpn_config=dict(type='str', required=True)
    )

    # Instantiate the AnsibleModule object
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Read the router configuration from the YAML file
    with open(module.params['router_config'], 'r') as f:
        router_config = yaml.load(f)

    # Read the switch configuration from the YAML file
    with open(module.params['switch_config'], 'r') as f:
        switch_config = yaml.load(f)

    # Read the VPN configuration from the YAML file
    with open(module.params['vpn_config'], 'r') as f:
        vpn_config = yaml.load(f)

    # Use the AnsibleModule to configure the network devices
    result = configure_network(router_config, switch_config, vpn_config)

    # Exit the module, passing the result
    module.exit_json(**result)

def configure_network(router_config, switch_config, vpn_config):
    # Create an Ansible inventory
    inventory = Inventory(['localhost'])

    # Create an Ansible runner for router
    runner = Runner(
        module_name='ios_config',
        module_args='src={}'.format(router_config),
        inventory=inventory,
        pattern='localhost'
    )

    # Run the Ansible module for router
    result = runner.run()

    # check if the configuration of router successful
    if result is None or result['localhost']['failed']:
        return dict(
            changed=False,
            message="Failed to configure the router"
        )

    # Create an Ansible runner for switch
    runner = Runner(
        module_name='ios_config',
        module_args='src={}'.format(switch_config),
        inventory=inventory,
        pattern='localhost'
    )

    # Run the Ansible module for switch
    result = runner.run()

    # check if the configuration of switch successful
    if result is None or result['localhost']['failed']:
        return dict(
            changed=False,
            message="Failed to configure the switch"
        )

    # Create an Ansible runner for VPN
    runner = Runner(
        module_name='ios_config',
        module_args='src={}'.format(vpn_config),
        inventory=inventory,
        pattern='localhost'
    )

    # Run the Ansible module for VPN
    result = runner.run()

    # check if the configuration of vpn successful
    if result is None or result['localhost']['failed']:
        return dict(
            changed=False,
            message="Failed to configure the VPN"
        )

    return dict(
        changed=True,
        message="Network configuration successful"
    )

def main():
    run_module()

if __name__ == '__main__':
    main()
