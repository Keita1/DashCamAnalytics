import pymongo
DB_NAME = "visiondb"

class VisionDB():
    def __init__(self,args):
        self.db = pymongo.MongoClient()[DB_NAME]

    def get_videos(self):
        pass

    def get_frames(self):
        pass
