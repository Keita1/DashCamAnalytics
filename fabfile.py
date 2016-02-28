import os,logging
from fabric.state import env
from fabric.api import task,local,run,put,get,lcd,cd,sudo
import boto,time
from boto.s3.key import Key
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')
import config
from config import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]

s3_connection = boto.connect_s3()

@task
def get_frames():
    bucket = s3_connection.get_bucket(config.BUCKETNAME)
    videos = [line.strip().split(" ")[-1] for line in file("dashcamlib/videos.txt") if line.strip().endswith(".mp4")]
    for i,v in enumerate(videos):
        key = bucket.get_key(v)
        name = v.split("/")[-1].split(".")[0]
        url = key.generate_url(expires_in=600)
        time.sleep(5)
        command = 'ffmpeg -ss 60 -to 600 -i "{}" -vf fps=1/60 temp/{}.%04d.png'.format(url,name)
        print command
        os.system(command)



@task
def server(rlocal=False):
    """
    start server
    """
    if rlocal:
        local('python server.py')
    else:
        run('python server.py')

@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()

