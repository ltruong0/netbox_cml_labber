from dotenv import load_dotenv
import os

load_dotenv()
NETBOX_URL = os.getenv('NETBOX_URL')
NETBOX_TOKEN = os.getenv('NETBOX_TOKEN')