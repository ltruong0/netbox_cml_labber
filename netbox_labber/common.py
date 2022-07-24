from dotenv import load_dotenv
from .utils import parse_args
import os

load_dotenv()
args = parse_args()
NETBOX_URL = os.getenv('NETBOX_URL')
NETBOX_TOKEN = os.getenv('NETBOX_TOKEN')