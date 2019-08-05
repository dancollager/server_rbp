from flask import Flask,jsonify
import os
import subprocess
# App of example for remote control
# 2019 forense
# Felipe-Leidy-Daniel
app = Flask(__name__)

@app.route('/devices')
def list_devices():
    cmd = "ls -l /dev/sd* 2>null | wc | awk '{print $1}' > /tmp/server/devices.txt"
    os.system(cmd)
    x = open('/tmp/server/devices.txt','r')
    line = x.readlines()
    x.close()
    if(int(line[0][:-1]) > 0):
        cmd="lsblk | egrep -o sd[^:]* | awk '{print $1}' > /tmp/server/listDevices.txt"
        os.system(cmd)
        x= open('/tmp/server/listDevices.txt','r')
        line = x.readlines()
    else:
        line = [0]
    return jsonify(
	devices=line,
	action="list"
	)
@app.route('/setrw/<device>')
def setWrite(device):
    # set device how rw and mount in media
    cmd = "blockdev --setrw /dev/"+str(device)
    os.system(cmd)
    cmd = "mount /dev/"+str(device)+" /media/"
    os.system(cmd)
    return jsonify(
        response="mounted successful"
        )
@app.route('/umount')
def umount():
    cmd = "umount /media"
    os.system(cmd)
    return jsonify(
        response="umounted successful"
    )
@app.route('/getImage/<device>/<status>')
def getImage(device, status):
    # use dd and copy the image
    # if status is true all process go to media else to the microSD
    if(status=="true"):
       # image with dd
       cmd = "dd if=/dev/"+device+" of=/media/"+device +".dd bs=10M"
       os.system(cmd)
       # copy of image
       cmd = "cp /media/" + device +".dd /media/copy-"+device+".dd"
       os.system(cmd)
       # hash of image
       cmd = "md5sum /media/"+device+".dd > /media/hash-"+device +".txt"
       os.system(cmd)
       # hash of copy image
       cmd = "md5sum /media/copy-"+device+".dd >> /media/hash-"+device+".txt"
       os.system(cmd)
    else:
       # image with dd
       cmd = "dd if=/dev/"+device+" of=/home/swb/images/"+device +".dd bs=10M"
       os.system(cmd)
       # copy of image
       cmd = "cp /home/swb/images/" + device +".dd /home/swb/images/copy-"+device+".dd"
       os.system(cmd)
       # hash of image
       cmd = "md5sum /home/swb/images/"+device+".dd > /home/swb/hash/hash-"+device +".txt"
       os.system(cmd)
       # hash of copy image
       cmd = "md5sum /home/swb/images/copy-"+device+".dd >> /home/swb/hash/hash-"+device+".txt"
       os.system(cmd)
    return jsonify(
       response="in process"
    )
@app.route('/detailImage/<device>/<status>')
def detailImage(device, status):
    if(status=="true"):
       cmd="fsstat /media/"+device+".dd > /tmp/server/detail.txt"
       os.system(cmd)
    else:
       cmd="fsstat /home/swb/images/"+device+".dd > /tmp/server/detail.txt"
       os.system(cmd)
    x = open('/tmp/server/detail.txt', 'r')
    line= x.readlines()
    return jsonify(
        response=line
    )
@app.route('/photorec/<device>/<status>')
def photo(device, status):
    if(status=="true"):
      cmd = "mkdir"
      os.system(cmd)
      cmd = "photorec /debug /d /media/recovered/ /log /cmd /media/copy-"+device +".dd options,mode_ext2,5,search"
      os.system(cmd)
    else:
      cmd = "mkdir /home/swb/recovered/"+device
      os.system(cmd)
      cmd = "photorec /debug /d /home/swb/recovered/"+device+"/ /log /cmd /home/swb/images/copy-"+device+ ".dd options,mode_ext2,5,search"
      os.system(cmd)
    return jsonify(
       response="recovered"
    )
