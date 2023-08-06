import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils

class imageFilter:
    def __init__(self):
        pass

    def median(self,datadir,targetdir):
        """Median filtering is similar to averaging, but the central pixel is
         replaced with the median value. This kind of filter is good for reducing
          static or salt and pepper noise in images. One benefit of the median filter
          is that it retains the edges of an image."""
        try:
          if not os.path.exists(targetdir+"/median"):
            os.mkdir(targetdir+"/median")
        except Exception as err:
            print("Error occurred while creating folder")

        for image in list(os.listdir(datadir)):
          img = cv2.imread(datadir+"/"+image)
          if img is not None:
            try:
              median = cv2.medianBlur(img, 5)
              plt.imsave(targetdir+"/median/median-"+image, cv2.cvtColor(median, cv2.COLOR_RGB2BGR))
            except Exception as e:
              print("Error occured in Median filter") 

    def laplacian(self,datadir,targetdir):
        try:
          if not os.path.exists(targetdir+"/laplacian"):
            os.mkdir(targetdir+"/laplacian")
        except Exception as err:
            print("Error occurred while creating folder")

        for image in list(os.listdir(datadir)):
          img = cv2.imread(datadir+"/"+image)
          if img is not None:
            try:
              lap = cv2.Laplacian(img,cv2.CV_64F)
              cv2.imwrite(targetdir+"/laplacian/laplacian-"+image,lap)
            except Exception as e:
              print("Error occured in laplacian filter")
        return

    def gaussian(self,datadir,targetdir):
        """Gaussian blurring looks at each pixel, then replaces
        that pixel value with the pixel value times the value drawn
        from the Gaussian distribution made by the pixels around it.
        You must specify the standard deviation in the x and y directions.
        A higher standard deviation leads to more blur."""
        try:
          if not os.path.exists(targetdir+"/gaussian"):
            os.mkdir(targetdir+"/gaussian")
        except Exception as err:
            print("Error occurred while creating folder")

        for image in list(os.listdir(datadir)):
          img = cv2.imread(datadir+"/"+image)
          if img is not None:
            try:
              gb = cv2.GaussianBlur(img, (3, 3), 1, 1)
              cv2.imwrite(targetdir+ "/gaussian/gaussian-" + image, gb)
            except Exception as e:
              print("Error occured in gaussian filter")
        return

    def bilateral(self,datadir,targetdir):
        """The bilateral filter is similar to the Gaussian filter,
        but if pixels are only filtered if they are ‘spatial neighbors’.
        That is, if the neighbor pixels are too different from the
         center pixel, the neighbor pixel will not be added to the
         Gaussian filter. Similar neighbors will still be used for filtering.
         This means that the bilateral filter performs Gaussian filtering, but preserves edges."""
        try:
          if not os.path.exists(targetdir+"/bilateral"):
            os.mkdir(targetdir+"/bilateral")
        except Exception as err:
            print("Error occurred while creating folder")

        for image in list(os.listdir(datadir)):
          img = cv2.imread(datadir+"/"+image)
          if img is not None:
            try:
              bilateral = cv2.bilateralFilter(img, 9, 75, 75)
              plt.imsave(targetdir+"/bilateral//bilateral-"+image,bilateral)
            except Exception as e:
              print("Error occured in bilateral filter")
        return