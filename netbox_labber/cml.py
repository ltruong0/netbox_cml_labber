from virl2_client import ClientLibrary

def cml_connect(url, username, password):
    # cml connection
    client = ClientLibrary(url=url, username=username,
                           password=password, ssl_verify=False)
    client.is_system_ready(wait=True)

    return client

def bulk_create_nodes(node_info_list, lab, x_origin=0, y_origin=0, x_offset=0, y_offset=0):
    ''''''
    x = x_origin
    y = y_origin

    for node_info in node_info_list:
        node_definition = node_info.get('node_definition')
        label = node_info.get("label")
        role = node_info.get("role")

        lab.create_node(label=label, node_definition=node_definition, x=x, y=y)
        
        # node_info['lab_node'] = lab.create_node(label=label, node_definition=node_definition, x=x, y=y)

        x += x_offset
        y += y_offset

