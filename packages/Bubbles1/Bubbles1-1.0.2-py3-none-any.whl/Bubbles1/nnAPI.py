

import os, glob
import subprocess, threading, time
import json

from shutil import copyfile

import cv2
import requests, json

def DrawBoxes(inFile, outFile, boxes):
    image = cv2.imread(inFile)
    
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.6
    thickness = 2
    for box in boxes:
        x1 = int(box["boundingBoxX"])
        y1 = int(box["boundingBoxY"])
        x2 = int(box["boundingBoxX"] + box["boundingBoxWidth"])
        y2 = int(box["boundingBoxY"] + box["boundingBoxHeight"])
        logo = box["logoResourceId"]
        conf = box["confidence"]
        boxColor = [0, 255, 0]
        if logo =='bulls':
            boxColor = [0, 0, 255] # red in BGR
        elif logo =='cans':
            boxColor = [255, 0, 0] # blue in BGR
        elif logo =='wfl':
            boxColor = [255, 0, 255] # Fuchsia in BGR
        
        cv2.rectangle(image, (x1, y1), (x2, y2), boxColor, 2)
        text = "{}: {:.4f}".format(logo, conf)
        
        
        textSize, baseline = cv2.getTextSize( text, fontFace, fontScale, thickness)
        baseline += thickness
        y1 -= baseline
        cv2.rectangle(image, (x1, y1+baseline), (x1+textSize[0]+2, y1-(textSize[1]+2)), boxColor, -1)
        cv2.putText(image, text, (x1+2, y1), fontFace, fontScale, [255,255,255], thickness)
    cv2.imwrite(outFile, image)
    
def UpdateCSV(file_name, detections, resultsFile, framerate):
    basename = os.path.basename(file_name)
    idx = float(basename[2:8])
    ts = (idx-1)/framerate
    for detection in detections:
        resultsFile.write('%s;%d;%d;%d;%d;%f;%s;%f\n' %(basename,
                                              round(detection['boundingBoxX']),
                                              round(detection['boundingBoxY']),
                                              round(detection['boundingBoxWidth']),
                                              round(detection['boundingBoxHeight']),
                                              detection['confidence'],
                                              detection['logoResourceId'],
                                              ts))

    
def get_jwt_token(uat_prefix, userid, password):
    print(f'Certs are at {requests.certs.where()}')
    url = "https://"+uat_prefix+"auth.kinetiq.tv/v1/auth/signin"

    payload = "{\n\tuserid:\"" + userid + "\",\n\tpassword:\"" + password + "\",\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify = False)
    if response.ok == True:
        r = json.loads(response.text)
        return r["data"]["accessToken"]
    else:
        print(response.reason)
        r = json.loads(response.text)
        print(r["errors"]["userId"][0])

        return "invalid"


def run(cmd, logfile):
    p = subprocess.Popen(cmd, shell=True, universal_newlines=True,stdout=logfile)
    ret_code = p.wait()
    logfile.flush()
    return ret_code

nnmodel = ''

def process(uat_prefix, jwt_token, outdir, file_name, resultsFile, framerate, detectorModel, limit):
    global nnmodel
    useCurl = False
    image = os.path.splitext(file_name)[0] + ".jpg"
    det = os.path.splitext(file_name)[0] + ".json"

    url = f'https://{uat_prefix}neural.kinetiq.tv/api/v1/detect?detectorModel={detectorModel}&limit={limit}'
    #url += '?cascadeMode=1'
    cmd = f'curl -H "Authorization: Bearer {jwt_token}" --location --request POST {url} --form imageFile=@{file_name} --silent'
    files = {'imageFile': open(file_name,'rb')}

    out_file = outdir + "/" + os.path.basename(file_name)
    tmp_file = out_file + ".json"

    retry_count = 0

    while True:
        if not useCurl:
            files = {'imageFile': open(file_name,'rb')}
            response = requests.request("POST", url, headers={'Authorization': f'Bearer {jwt_token}'}, files=files)
            if response.ok == True:
                detection_result = json.loads(response.text)
                #model = os.path.splitext(detection_result["neuralNetModel"]["version"].split("/")[2])[0]
                model = os.path.splitext(os.path.basename(detection_result["neuralNetModel"]["modelName"]))[0]
                if nnmodel != model:
                    nnmodel = model
                    print(f'API uses {nnmodel} model')
                break
            else:
                 print(f'Retrying using {url}, reason: {response.reason}, {response.text}')

                 if retry_count == 10:
                     print('Fatal error')
                     exit(1)

        else:
            with open(tmp_file,"w") as outp:
                run(cmd,outp)

            # read in tmp.json
            with open(tmp_file,"r") as f:
                try:
                    detection_result = json.load(f)

                    # get model, for now use version info
                    # model = os.path.splitext(detection_result["neuralNetModel"]["version"].split("/")[2])[0]
                    model = os.path.splitext(os.path.basename(detection_result["neuralNetModel"]["modelName"]))[0]
                    if nnmodel != model:
                        nnmodel = model
                        print(f'API uses {nnmodel} model')
                    break
                except:
                    print('Failure using: '+url)

                    if retry_count == 10:
                        print('Fatal error')
                        exit(1)
        retry_count = retry_count + 1


    if len(detection_result["logoIdentifications"]) > 0:
        DrawBoxes(file_name, out_file, detection_result["logoIdentifications"])
        UpdateCSV(file_name, detection_result["logoIdentifications"], resultsFile, framerate)
       
    if useCurl:
        os.remove(tmp_file)

    return

def ProcessAll(uat_prefix, jwt_token, batchSize, nnImagesAbsPath, rawImagesAbsPath, framerate, detectorModel, limit):
    files = glob.glob(f'{rawImagesAbsPath}/*.jpg')
    if batchSize <=1:
        for f in files:
            print("Process file: " + f)
            process(uat_prefix ,jwt_token, nnImagesAbsPath, f)
        return
    csv_file = nnImagesAbsPath + '/neuralnetResults.csv'
    f = open(csv_file, "w")
    f.write('filename;x;y;w;h;conf;label;time\n')

    # Multithread processing    
    i = 0
    threads = []
    prev = start = time.perf_counter()
    for i in range(len(files)):
        threads.append(threading.Thread(target=process,
            args = (uat_prefix ,jwt_token, nnImagesAbsPath, files[i], f, framerate, detectorModel, limit)))
        if i==len(files) - 1 or len(threads) == batchSize:
            for t in threads:
                t.daemon=True
                time.sleep(0.001)
                t.start()
            for t in threads:
                t.join()
            cur = time.perf_counter()
            print(f'processed {i} of {len(files)}, batch of {len(threads)}, avr {int(i/(cur-start))}fps, cur {int(len(threads)/(cur-prev))}fps')
            prev = cur
            threads = []
    f.close()
