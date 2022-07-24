import pynetbox
from virl2_client import ClientLibrary
import logging
import sys

# convert platform to a node definition available
platform_to_node_def = {
    None : "unmanaged_switch", # default for non platform?
    'cisco-ios': 'iosv'
}

def create_logger():
    # create logger
    logger = logging.getLogger('main')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    return logger

def netbox_connect(url, token):
    ''''''
    # add exception handling
    nb = pynetbox.api(url,token)
    return nb

def cml_connect(url,username,password):
    # cml connection
    client = ClientLibrary(url=url, username=username, password=password, ssl_verify=False)
    client.is_system_ready(wait=True)

    return client

def bulk_create_nodes(node_info_list, lab, x_origin=0, y_origin=0, x_offset=0, y_offset=0):
    ''''''

    x = x_origin
    y = y_origin

    for node_info in node_info_list:
        node_definition = platform_to_node_def[node_info.get('platform')]
        label = node_info.get("label")
        role = node_info.get("role")

        logger.info(f'Label : {label}\nRole : {role}\nNode Definition : {node_definition}')
        node_info['lab_node'] = lab.create_node(label=label, node_definition=node_definition, x=x, y=y)

        x += x_offset
        y += y_offset


def main():
    nb = netbox_connect(url='https://demo.netbox.dev/', token="e55d10d74016d4d437b9f3840b5efc28b3301863")

    # convert to dict and add to list
    # devices
    devices = nb.dcim.devices.all()
    devices = [dict(device) for device in devices]
    
    # cables
    cables = nb.dcim.cables.all()
    cables = [dict(cable) for cable in cables]

    # cml connection
    client = cml_connect(url="https://10.10.20.161", username="developer", password="C1sco12345")

    nodes = {}

    for device in devices:

        platform = device.get('platform')
        device_role = device.get('device_role')

        if platform:
            platform = device['platform'].get('slug')
        
        if device_role:
            device_role = device['device_role'].get('slug')

        nodes[device['name']] = {
            'label' : device.get('name'),
            'role' : device_role,
            'platform' : platform,
        }


    # create lab
    lab = client.create_lab(title='new lab')
    
    # router nodes
    logger.info("Creating Router Nodes")
    router_nodes = [node_info for label, node_info in nodes.items() if node_info.get('role') in ['router']]
    bulk_create_nodes(node_info_list=router_nodes,lab=lab,x_offset=180)

    # distribution switch nodes
    dist_switch_nodes = [node_info for label, node_info in nodes.items() if node_info.get('role') in ['distribution-switch']]
    bulk_create_nodes(node_info_list=dist_switch_nodes,lab=lab,y_origin=-200, x_offset=180)

    # access switch nodes
    access_switch_nodes = [node_info for label, node_info in nodes.items() if node_info.get('role') in ['access-switch']]
    bulk_create_nodes(node_info_list=access_switch_nodes,lab=lab,y_origin=-300, x_offset=180)


    device_nodes_dict = {}
    for router_node in router_nodes:
        device_nodes_dict[router_node['label']] = router_node

    for dist_switch_node in dist_switch_nodes:
        device_nodes_dict[dist_switch_node['label']] = dist_switch_node

    for access_switch_node in access_switch_nodes:
        device_nodes_dict[access_switch_node['label']] = access_switch_node

    # cables

    # physical links
    physical_links = [cable for cable in cables if cable['termination_a_type'] == 'dcim.interface' and cable['termination_b_type'] == 'dcim.interface']

    for physical_link in physical_links:
        a_termination = device_nodes_dict.get(physical_link['termination_a']['device']['name'])
        b_termination = device_nodes_dict.get(physical_link['termination_b']['device']['name'])

        if a_termination and b_termination:
            print(physical_link['termination_a']['device']['name'])
            print(physical_link['termination_b']['device']['name'])
            lab.create_link(a_termination['lab_node'].create_interface(), b_termination['lab_node'].create_interface())


if __name__ == '__main__':
    logger = create_logger()
    main()

