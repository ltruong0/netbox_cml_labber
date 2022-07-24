from netbox_labber.utils import create_logger
from netbox_labber.netbox import netbox_connect
from netbox_labber.cml import cml_connect
from netbox_labber import common

# convert platform to a node definition available
platform_to_node_def = {
    None: "unmanaged_switch",  # default for non platform?
    'cisco-ios': 'iosv'
}

logger = create_logger()

def main():
    nb = netbox_connect(url=common.NETBOX_URL,
                        token=common.NETBOX_TOKEN)

    # convert to dict and add to list
    # devices
    devices = nb.dcim.devices.all()
    devices = [dict(device) for device in devices]

    # cables
    cables = nb.dcim.cables.all()
    cables = [dict(cable) for cable in cables]

    nodes = {}

    for device in devices:

        platform = device.get('platform')
        device_role = device.get('device_role')

        if platform:
            platform = device['platform'].get('slug')

        if device_role:
            device_role = device['device_role'].get('slug')

        nodes[device['name']] = {
            'label': device.get('name'),
            'role': device_role,
            'platform': platform,
            'node_definition': platform_to_node_def.get(platform)
        }

    # all nodes
    device_nodes = [node_info for label, node_info in nodes.items()]
    device_nodes_dict = {}
    for device_node in device_nodes:
        device_nodes_dict[device_node['label']] = device_node

    # physical links
    physical_links = [cable for cable in cables if cable['termination_a_type']
                      == 'dcim.interface' and cable['termination_b_type'] == 'dcim.interface']

    lab_config_dict = {
        "lab": {
            "lab_notes": "",
            "lab_title": "new lab",
            "lab_description": "",
            "lab_owner": "developer",
        },
        "nodes": [{"data": device_node} for device_node in device_nodes],
        'links': [],
    }

    for physical_link in physical_links:
        a_termination = device_nodes_dict.get(
            physical_link['termination_a']['device']['name'])
        b_termination = device_nodes_dict.get(
            physical_link['termination_b']['device']['name'])

        if a_termination and b_termination:
            lab_config_dict['links'].append({
                "data": {
                    'interface_a': {
                        'device': a_termination['label'],
                        'int_name': physical_link['termination_a']['name']
                    },
                    'interface_b': {
                        'device': b_termination['label'],
                        'int_name': physical_link['termination_b']['name']
                    },
                }})

    logger.info(lab_config_dict)
    # cml connection
    # client = cml_connect(url="https://10.10.20.161",
    #                      username="developer", password="C1sco12345")
    # create lab
    # lab = client.create_lab(title='new lab2')
    # lab.create_interface
    # bulk_create_nodes(node_info_list=device_nodes,lab=lab,x_offset=180)


if __name__ == '__main__':
    main()
