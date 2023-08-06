#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 17:47:00 2021

@author: kinetiqtvsoftwareservices
"""

import argparse, csv, glob, sys, shutil, time
import subprocess
import os.path
import requests, json
import os
from Bubbles1 import nnAPI
from nnAPI import *


try:
    import cv2
    import numpy as np
    opencvPresent = True;
except ImportError:
    print('WARNING!!! OpenCV is unavailable (did you run "pip install opencv-python"?). Drawing will be disabled')
    opencvPresent = False;

def DetectFramerate(filename):
    if not opencvPresent:
        raise Exception("OpenCV not installed, framerate cannot be estimated")
    cap = cv2.VideoCapture()
    cap.setExceptionMode(False)
    if not cap.open(filename):
        raise Exception('Failed opening file: ' + str(filename))
        cap.release()
    ret, image = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        raise Exception("Can't receive frame (stream end?). Exiting ...")
        sys.exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def SliceVideo(config):
    start = time.perf_counter()
    if os.path.isdir(config["rawImages"]):
        shutil.rmtree(config["rawImages"])
    os.makedirs(config["rawImages"])
    cmd = f'ffmpeg -i "{config["input"]}" -r {config["framerate"]} -vf scale=ih*dar:ih -q:v 2 {config["rawImages"]}/im%06d.jpg -y'
    print (cmd)    
    #subprocess.run(cmd);
    os.system(cmd)
    print(f'SliceVideo done in {time.perf_counter() - start} seconds')


def ProcessWithNeuralNet(config):
    print(f'Starting ProcessWithNeuralNet...')
    start = time.perf_counter()
    if os.path.isdir(config["nnImages"]):
        shutil.rmtree(config["nnImages"])
    os.makedirs(config["nnImages"])
    
    CLIdir = os.path.dirname(config["nnCLI"])
    rawImagesAbsPath = os.path.abspath(config["rawImages"])
    nnImagesAbsPath  = os.path.abspath(config["nnImages"])

    if config["nnIsAPI"] == 0:
        
        script_dir = os.getcwd()
        os.chdir(CLIdir)
        
        cmd = f'{os.path.basename(config["nnCLI"])} -i "{rawImagesAbsPath}" -o "{nnImagesAbsPath}"'
        cmd += f' -d 2 -c 0 -t 0.5 -limit {config["nnAPI_limit"]} -detectorModel {config["nnAPI_detectorModel"]}'
        print (cmd)    
        
        subprocess.run(cmd);
        
        os.chdir(script_dir) # return back to original dir
    else:
        jwt_token = nnAPI.get_jwt_token(config["nnAPI_uat_prefix"], config["nnAPI_user"], config["nnAPI_pwd"])
        nnAPI.ProcessAll(config["nnAPI_uat_prefix"], jwt_token, config["nnAPI_batchSize"], nnImagesAbsPath, rawImagesAbsPath, config["framerate"], config["nnAPI_detectorModel"], config["nnAPI_limit"])
    print(f'ProcessWithNeuralNet done in {time.perf_counter() - start} seconds')

def CopyAllFiles(src, dst):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst)

def CreateQAedCSVFile(removedFiles, nnResultsFileName, qaResultsFileName):
    with open(nnResultsFileName, newline='') as nnResultsFile, open(qaResultsFileName, 'w', newline='') as qaResultsFile:
      reader = csv.reader(nnResultsFile, delimiter=';')
      writer = csv.writer(qaResultsFile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
      for row in reader:
        if row[0] in removedFiles:
          continue
        writer.writerow(row)
        
def DoQA(config):
    if os.path.isdir(config["qaImages"]):
        shutil.rmtree(config["qaImages"])
    os.makedirs(config["qaImages"])
    CopyAllFiles(config["nnImages"], config["qaImages"])
    files = glob.glob(f'{config["qaImages"]}/*.jpg')
    if len(files) == 0:
        raise Exception(f'{config["qaImages"]} has no images. QA is not possible')
    
    print(f' QA in process for {len(files)} files')
    print(f' <-, -> or L, R to advance previous/next file')
    print(f' Del or X to delete false positive file. IF YOU MADE AN ERROR, IT CANNOT BE UNDONE WITHOUT REPROCESSING!!!')
    print(f' Esc to stop')
    
    win_w = 1024
    win_h = 576
    
    cv2.namedWindow("Frame")
    #cv.setMouseCallback("Frame", mouse_click, ["Full", clear1, KP1, TB1])
    cur = 0
    keepProcessing = True
    removedFiles = []
    while keepProcessing: 
        cur = cur % len(files)
        filename = files[max(min(cur, len(files)-1), 0)]
        print(filename)
        if not os.path.isfile(filename):
            cur += inc
            continue
        cv2.setWindowTitle("Frame", f'{cur+1}/{len(files)}: {os.path.basename(filename)}')
        im = cv2.resize(cv2.imread(filename), (win_w, win_h), interpolation = cv2.INTER_AREA )
        cv2.imshow("Frame", im)
        
        while True:
            k = cv2.waitKeyEx(0)
            if k==config["qaEsc"] or k==-1: # Esc or window closed
                print(f'Exiting QA mode')
                keepProcessing = False
                break
            elif k==config["qaRight"] or k==ord('r') or k==ord('R'):
                cur += 1
                break
            elif k==config["qaLeft"] or k==ord('l') or k==ord('L'):
                cur -= 1
                break
            elif k==config["qaDel"] or k==ord('x') or k==ord('X'):
                print(f'deleting {filename}')
                os.remove(filename)
                files.pop(cur)
                removedFiles.append(os.path.basename(filename))
                break
            else:
                print(f'unknown key {k} pressed. Ignoring') 
    cv2.destroyAllWindows()
    CreateQAedCSVFile(removedFiles, os.path.abspath(config["nnImages"])+'/neuralnetResults.csv', config["output"]+'.csv')
    
#    cmd = f'start /WAIT {config["qaImages"]}/im000002.jpg'
#    print (cmd)    
#    
#    # print(subprocess.run(cmd, shell=True));
#    proc = subprocess.Popen(cmd, shell=True)
#    print(proc)
#    proc.wait(10000)
#    print(proc)
#    proc.kill()
#    print(proc)
#    #print(os.system(cmd))
#    #subprocess.run('TempFiles\QAed\im000002.jpg');


def CombineImages(config):
    start = time.perf_counter()
    if os.path.isdir(config["combinedImages"]):
        shutil.rmtree(config["combinedImages"])
    os.makedirs(config["combinedImages"])
    # copy original frames
    CopyAllFiles(config["rawImages"], config["combinedImages"])
    # overwrite some with QAed frames
    CopyAllFiles(config["qaImages"], config["combinedImages"])
    print(f'CombineImages done in {time.perf_counter() - start} seconds')

            
def ProduceMP4(config):
    start = time.perf_counter()
    cmd =  f'ffmpeg -f image2 -r {config["framerate"]} -i "{config["combinedImages"]}/im%06d.jpg" '
    cmd += f' -i "{config["input"]}" -map 0:v -map 1:a "{config["output"]}" -y'
    print (cmd)    
    os.system(cmd);
    print(f'ProduceMP4 done in {time.perf_counter() - start} seconds')


   
