__author__ = 'aub3'
import platform,os
from appcode import app

if __name__ == '__main__':
    app.debug = True
    app.run(port=9500)