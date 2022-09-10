from operator import truediv
import cv2
import sys
from PIL import Image
import time
import os
import mimetypes
import imageio_ffmpeg
from tqdm import tqdm 
mimetypes.init()
col= os.get_terminal_size().columns
line = os.get_terminal_size().lines
aspect_ratio = None
import shutil
def imageToASCII(imagePath:str,fps):
    img = Image.open(imagePath)
    global aspect_ratio
    width, height = img.size
    if aspect_ratio == None:
        aspect_ratio = height/width

    new_width = 140
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')
    pixels = img.getdata()
    chars = ["B","S","#","&","@","$","%","*","!",":","."]
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    l = len(ascii_image)

    for i in range(len(ascii_image)):
        diff = col - len(ascii_image[i])
        for a in range(diff):
            ascii_image[i] += " "
    ascii_image = "".join(ascii_image)    
    time.sleep(fps)
    print("\n\n"+ascii_image, end = "\r")
    
def videoToFrames(name:str):
    os.mkdir("folder")
    vidcap = cv2.VideoCapture(name)
    frames,sec = imageio_ffmpeg.count_frames_and_secs(name)
    fps = int(frames)/int(sec)
    
    success,image = vidcap.read()
    count = 0
    for i in tqdm(range(frames)):
        cv2.imwrite("folder/frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
    for i in range(count):
        imageToASCII("./folder/frame"+str(i)+".jpg",1/int(fps))
    shutil.rmtree("folder",ignore_errors=True)
def main():
    
    args = sys.argv
    path = str(args[1])
    print(path)

    if path != None:
        shutil.rmtree("folder",ignore_errors=True)

        if "video" in mimetypes.guess_type(path)[0]:
            videoToFrames(path)
        elif "image" in  mimetypes.guess_type(path)[0]:
            imageToASCII(path,0.01)
if __name__=="__main__":
    main()
