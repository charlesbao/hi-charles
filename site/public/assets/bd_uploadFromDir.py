#coding: utf-8
import os,json,sys,tempfile
from baidupcsapi import PCS
import progressbar

class ProgressBar():
    def __init__(self):
        self.first_call = True
    def __call__(self, *args, **kwargs):
        if self.first_call:
            self.widgets = [progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker('>')),
                            ' ', progressbar.FileTransferSpeed()]
            self.pbar = progressbar.ProgressBar(widgets=self.widgets, maxval=kwargs['size']).start()
            self.first_call = False

        if kwargs['size'] <= kwargs['progress']:
            self.pbar.finish()
        else:
            self.pbar.update(kwargs['progress'])


def upload(filePath,remotePath):
    fid = 1
    md5list = []

    with open(filePath, 'rb') as infile:
        while 1:
            data = infile.read(chunkSize)
            if len(data) == 0: break
            smallfile = os.path.join(tmpDir, 'tmp%d' % fid)
            with open(smallfile, 'wb') as f:
                f.write(data)
            print('chunk%d size %d' % (fid, len(data)))
            fid += 1
            print('start uploading...')
            ret = pcs.upload_tmpfile(open(smallfile, 'rb'), callback=ProgressBar())
            md5list.append(json.loads(ret.content)['md5'])
            print('md5: %s' % (md5list[-1]))
            os.remove(smallfile)

    os.rmdir(tmpDir)
    pcs.upload_superfile(os.path.join(remotePath,os.path.basename(filePath)), md5list)

pcs = PCS('18661168001','Carl656693')
chunkSize = 1024*1024*256
tmpDir = tempfile.mkdtemp('bdpcs')
remotePath = "/yunbeifeng"

for each in os.listdir('upload'):
    print 'upload',each
    upload(os.path.join('upload',each),remotePath)
    print 'finish',each


