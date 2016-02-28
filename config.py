import sys
BUCKETNAME = "aub3cardata"
PREFIX = "test"
USER = "ubuntu"
HOST = "52.90.249.222"
private_key =  "~/.ssh/cs5356"
CONFIG_PATH = __file__.split('settings.py')[0]
AWS = sys.platform != 'darwin'
