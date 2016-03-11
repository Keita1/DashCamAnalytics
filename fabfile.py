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
from config import USER,private_key,HOST,TEMP_DIR
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]

s3_connection = boto.connect_s3()

@task
def get_frames():
    bucket = s3_connection.get_bucket(config.BUCKETNAME)
    try:
        os.mkdir("{}/temp".format(TEMP_DIR))
    except:
        pass
    videos = [line.strip().split(" ")[-1] for line in file("data/videos.txt") if line.strip().endswith(".mp4")]
    for i,v in enumerate(videos):
        key = bucket.get_key(v)
        name = v.split("/")[-1].split(".")[0]        # url = key.generate_url(expires_in=600)
        with open("{}/temp.mp4".format(TEMP_DIR),'w') as fh:
            key.get_contents_to_file(fh)
        for i in range(1000):
            command = 'ffmpeg -accurate_seek -ss {} -i {}/temp.mp4   -frames:v 1 {}/temp/{}.{}.jpg'.format(15.0*i,TEMP_DIR,TEMP_DIR,name,i)
            print command
            retval = os.system(command)
            if retval != 0:
                break
        os.system('cd {}/temp;aws s3 mv . s3://{}/frames/dataset/ --recursive --storage-class "REDUCED_REDUNDANCY"'.format(TEMP_DIR,config.BUCKETNAME))




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


@task
def setup():
    """
    Task for initial set up of AWS instance.
    """
    sudo("chmod 777 /mnt/")
    sudo("add-apt-repository ppa:kirillshkrogalev/ffmpeg-next")
    sudo("apt-get update")
    sudo("apt-get install -y ffmpeg")
    sudo("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927")
    sudo('echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list')
    sudo('apt-get update')
    sudo('apt-get install -y mongodb-org')
    try:
        sudo('service mongod start')
    except:
        pass
    try:
        run("rm -rf DashCamAnalytics")
    except:
        pass
    run("git clone https://github.com/AKSHAYUBHAT/DashCamAnalytics")
    with cd("DashCamAnalytics/appcode/db/dump/visiondb"):
        run("gzip -d *")
    run("mongorestore --db visiondb VisualSearchServer/appcode/db/dump/visiondb")



@task
def backup_db():
    with lcd("appcode/db"):
        local("rm -rf dump")
        local("mongodump --db visiondb")


@task
def get_videos():
    with cd("/mnt/video"):
        run('youtube-dl "https://www.youtube.com/playlist?list=PLccnpqMfP0kwx4qaj1ZZw9YJtTOptmBJJ" -o "%(epoch)s.%(ext)s" --ignore-errors')

@task
def get_frames():
    videos = """
    """
    for i,v in enumerate(videos.strip().split("\n")):
        v = v.strip()
        if v:
            for i in range(500):
                command = 'ffmpeg -accurate_seek -ss {} -i /mnt/video/{}   -frames:v 1 /mnt/frames/{}.{}.jpg'.format(15.0*i,v,v,i)
                retval = run(command)
                if retval.return_code != 0:
                    break
            run('cd /mnt/frames;aws s3 mv . s3://aub3data/nyc/frames/ --recursive --storage-class "REDUCED_REDUNDANCY"')
            run('cd /mnt/video/;aws s3 mv {} s3://aub3data/nyc/videos/ --storage-class "REDUCED_REDUNDANCY"'.format(v))

