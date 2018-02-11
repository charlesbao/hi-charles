import os
from oss2 import SizedFileAdapter, determine_part_size, Bucket, Auth
from oss2.models import PartInfo

def upload(filename,key):
    total_size = os.path.getsize(filename)
    part_size = determine_part_size(total_size, preferred_size=100 * 1024)

    END_POINT = 'oss-cn-shanghai.aliyuncs.com'
    AUTH = Auth('LTAIStvC4wpBWRVG', 'BNXtvOz82JjzlSLjPBdQJyEUpXi4PD')
    BUCKET_NAME = "yunbeifeng"
    bucket = Bucket(AUTH, END_POINT, bucket_name=BUCKET_NAME)

    upload_id = bucket.init_multipart_upload(key).upload_id
    parts = []
    with open(filename, 'rb') as fileobj:
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(key, upload_id, part_number,
                                        SizedFileAdapter(fileobj, num_to_upload))
            parts.append(PartInfo(part_number, result.etag))
            offset += num_to_upload
            part_number += 1

    bucket.complete_multipart_upload(key, upload_id, parts)

for each in os.listdir('upload'):
    print 'upload',each
    upload(os.path.join('upload',each),os.path.join('fc2live_video',each))
    print 'finish',each
