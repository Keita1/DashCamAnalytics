import sys
BUCKETNAME = "aub3cardata"
PREFIX = "test"
USER = "ubuntu"
HOST = "52.87.173.249"
private_key =  "~/.ssh/cs5356"
CONFIG_PATH = __file__.split('settings.py')[0]
AWS = sys.platform != 'darwin'
if AWS:
    TEMP_DIR = "/tmp/"
else:
    TEMP_DIR = "/Users/aub3/temp/"
