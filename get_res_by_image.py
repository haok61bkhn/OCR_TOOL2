import numpy as np
import requests
import cv2
import base64
import tqdm
link="http://45.122.253.30:1234/api"

def compare_strings(a,b):
    na=len(a)
    nb=len(b)
    f=np.zeros((na,nb))

    for i in range(na):
        if(a[i]!=b[0]):
            f[i][0]=i+1
        else : f[i][0]=i

    for i in range(nb):
        if(a[0]!=b[i]):
            f[0][i]=i+1
        else : f[0][i]=i   

    for i in range(1,na):
        for j in range(1,nb):
            if a[i]==b[j] :
                f[i][j]=f[i-1][j-1]
            else:
                f[i][j]=min(f[i-1][j-1],f[i-1][j],f[i][j-1])+1
    return f[na-1][nb-1]

def convert_to_b64(img):
    _, im_arr = cv2.imencode('.png', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return str(im_b64)[2:-1]

def get_res(path):
    img=cv2.imread(path)
    response = requests.post(link, json={"image":convert_to_b64(img)}).json()
    return response["id"]+"\n"+response["name"]+"\n"+response["date"]+"\n"+response["ad1"]+"\n"+response["ad2"]

import glob
import os
if __name__ == "__main__":
    datadir="image"
    predict_dir="predict"
    for x in tqdm.tqdm(glob.glob(datadir+"/*")):
        f=open(os.path.join(predict_dir,x.split("/")[-1].split(".")[0]+".txt"),"w+")
        f.writelines(get_res(x))
        f.close()
