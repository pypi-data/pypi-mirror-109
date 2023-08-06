import argparse
#from BubblesK.nnAPI import DrawBoxes, get_jwt_token, run, process, ProcessAll
#from NNDemo import SliceVideo, DetectFramerate, ProcessWithNeuralNet, CopyAllFiles, CreateQAedCSVFile, DoQA, CombineImages, ProduceMP4
import NNDemo
from NNDemo import *

def main():
    ap = argparse.ArgumentParser()
#  The only required parameter
    ap.add_argument("-i", "--input", type=str, required=True,
    help="input video file name")
# # optional parameters  
    ap.add_argument("-r", "--framerate", type=float, required=False, default=0,
    help="Framerate of processed video (select one of input stream for better results). 0 (default) - estimate with OpenCV")
    ap.add_argument("--output", type=str, required=False,
    help="Output video file name. Default is <input>_NN.mp4")
    ap.add_argument("--rawImages", type=str, required=False, default="TempFiles/Images",
    help="Temporary folder for raw sliced frames. Default is 'TempFiles/Images'")
    ap.add_argument("--nnImages", type=str, required=False, default="TempFiles/NN",
    help="Temporary folder for frames processed by Neural Net. Default is 'TempFiles/NN'")
    ap.add_argument("--qaImages", type=str, required=False, default="TempFiles/QAed",
    help="Temporary folder for frames accepted on QA step. Default is 'TempFiles/QAed'")
    ap.add_argument("--combinedImages", type=str, required=False, default="TempFiles/Combined",
    help="Temporary folder for raw putput frames. Default is 'TempFiles/Combined'")
    ap.add_argument("--nnIsAPI", type=int, required=False, default=1,
    help="Use NN API. If 0, will use CLI, Default is 1")
    ap.add_argument("--nnCLI", type=str, required=False, default='C:/Documents and Settings/Administrator/Documents/Val/NeuralNetEngine.CLI.GPU.3/NeuralNetEngine.CLI.exe',
    help="Path to NN CLI (only used if nnIsAPI==0). Default is 'C:/Documents and Settings/Administrator/Documents/Val/NeuralNetEngine.CLI.GPU.3/NeuralNetEngine.CLI.exe'")
    # NN API settings
    ap.add_argument("--nnAPI_uat_prefix", type=str, required=False, default="uat-", nargs='?', const='',
    help="Prefix before 'neural.kinetiq.tv'. Should be empty for Live, 'uat-' for UAT. Default is 'uat-'")
    ap.add_argument("--nnAPI_user", type=str, required=False, default="internal-api@kinetiq.tv",
    help="API username. Default is 'internal-api@kinetiq.tv'")
    ap.add_argument("--nnAPI_pwd", type=str, required=False, default="1549942b-d2f1-6957-652f-8abbf83afbe7",
    help="API password. Default is <....>")
    ap.add_argument("--nnAPI_batchSize", type=int, required=False, default=200,
    help="Number of parallel requests to API. 1 mean one-ny-one, more is faster nut may trigger backpressure. Default is 200")
    ap.add_argument("--nnAPI_detectorModel", type=str, required=False, default='d1',
    help="Detector model to use: d1 for default production, d2 for slow but more accurate. Default is d2")
    ap.add_argument("--nnAPI_limit", type=int, required=False, default=10,
    help="Max number of bounding boxes to report per frame. Default is 10")
    ap.add_argument("--qaLeft", type=int, required=False, default=2424832,
    help="Key code to go back in QA process. Default is 2424832 ( <- in Windows)")
    ap.add_argument("--qaRight", type=int, required=False, default=2555904,
    help="Key code to go forward in QA process. Default is 2555904 ( -> in Windows)")
    ap.add_argument("--qaDel", type=int, required=False, default=3014656,
    help="Key code to remove false detection in QA process. Default is 3014656 ( Del in Windows)")
    ap.add_argument("--qaEsc", type=int, required=False, default=27,
    help="Key code to exit QA process. Default is 27 ( Esc in Windows)")
        
    
    config = vars(ap.parse_args())
    
    
    
    
    
   # Set derived defaults 
    if config["output"] == None:
        config["output"] = config["input"] + "_NN.mp4"
    if(config["framerate"] == 0):
        config["framerate"] = DetectFramerate(config["input"])
        print(config)


    

#config={}
#config["input"] = args["input"]
#config["framerate"] = args["framerate"]  # convert video to this framerate
#config["output"] = config["input"] + "_NN.mp4"
#config["rawImages"] = "TempFiles/Images"
#config["nnImages"] = "TempFiles/NN"
#config["qaImages"] = "TempFiles/QAed"
#config["combinedImages"] = "TempFiles/Combined"
#config["nnIsAPI"] = True # use API (true) or local CLI (false)
#config["nnCLI"] = 'C:/Documents and Settings/Administrator/Documents/Val/NeuralNetEngine.CLI.GPU.3/NeuralNetEngine.CLI.exe'

#config["nnAPI_uat_prefix"] = '' #"uat-" # should be "" for Live, "uat-" for UAT
#config["nnAPI_user"] = "internal-api@kinetiq.tv"
#config["nnAPI_pwd"] = "1549942b-d2f1-6957-652f-8abbf83afbe7"
#config["nnAPI_batchSize"] = 200 # number of parallel requests to NN API

# Values below for left, right and Del are Windows specific. You may need to reassign them on other macines
#config["qaLeft"] = 2424832  # 0x250000
#config["qaRight"] = 2555904 # 0x270000
#config["qaDel"] = 3014656   # 0x2E0000
#config["qaEsc"] =  27


    SliceVideo(config)  
    ProcessWithNeuralNet(config)
    DoQA(config)
    CombineImages(config)
    ProduceMP4(config)

if __name__ == "__main__":
	main()    


