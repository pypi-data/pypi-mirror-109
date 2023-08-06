from PIL import Image
import math as m
import cv2 as cv
import ToVid
import os

def frame(dv):

  cap = cv.VideoCapture(dv)
  frames = []

  while cap.isOpened():
      rv,f = cap.read()
      
      if rv:
        frames.append(f)
      else:
        break

  return frames


def segment(dv):
  timestamps = []
  count = 0
  cap = cv.VideoCapture(dv)
  frames = []

  while cap.isOpened():
      rv,f = cap.read()
      
      if rv:
        timeMs = m.floor(cap.get(cv.CAP_PROP_POS_MSEC))
        count+=1

        frames.append({'frame':f,'offval':count,'offms':timeMs})
        
        
      else:
        break

  return frames

def segmentRangeMS(seg, s, e):
  out = []

  for dict in seg:
    if dict['offms'] >= s and dict['offms'] <= e:
      out.append(dict['frame'])

  return out

def segmentRangeOffSet(seg, s, e):
  out = []

  for dict in seg:
    if dict['offval'] >= s and dict['offval'] <= e:
      out.append(dict['frame'])

  return out

def vidToFolder(frames,outfolder):
  try:
    os.mkdir(outfolder)
  except:
    pass
  count = 0
  
  for f in frames:
    count+=1
    img = Image.fromarray(f)

    img.save(f'{outfolder}/frame{count}.png')

folderToVid = ToVid.folderToVid
    
    
  
      
  
  



