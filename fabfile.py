import os
from fabric.api import task
import boto,time
from boto.s3.key import Key

import config
s3_connection = boto.connect_s3()

@task
def get_frames():
    bucket = s3_connection.get_bucket(config.BUCKETNAME)
    videos = [line.strip().split(" ")[-1] for line in file("lib/videos.txt") if line.strip().endswith(".mp4")]
    for i,v in enumerate(videos):
        if i > 2:
            key = bucket.get_key(v)
            name = v.split("/")[-1].split(".")[0]
            url = key.generate_url(expires_in=600)
            time.sleep(5)
            command = 'ffmpeg -i "{}" -vf fps=1/60 temp/{}.%04d.png'.format(url,name)
            print command
            os.system(command)
            break



