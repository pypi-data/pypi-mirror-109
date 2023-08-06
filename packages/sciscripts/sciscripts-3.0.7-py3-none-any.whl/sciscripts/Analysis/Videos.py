#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20210614
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Functions for analyzing and manipulating video files.

Under heavy development, highly unstable.
"""

print('[Analysis.Videos] Importing dependencies...')
import cv2
import numpy as np
import os
from sciscripts.Analysis.Analysis import GetPeaks
from sciscripts.IO import Video
print('[Analysis.Videos] Done.')


# Level 0
def FrameScale(frame, downsampling=3):
    """
    Taken and modified from Justin Mitchel
    @ https://www.codingforentrepreneurs.com/blog/open-cv-python-change-video-resolution-or-scale
    """
    width = int(frame.shape[1]/downsampling)
    height = int(frame.shape[0]/downsampling)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def GetLedBlinkStart(File, Channel='r', Dur=10, Verbose=False):
    LedVideo, dvInfo = Video.Read(File)
    ChInd = {'r':2, 'g':1, 'b':0}

    # print('Get time offset...', end='')
    # Start = perf_counter()
    Ch = np.zeros(int(dvInfo['FPS']*Dur), dtype=float)
    for F in range(int(dvInfo['FPS']*Dur)):
        f, Frame = LedVideo.read()
        if not f: break
        Ch[F] = Frame[:,:,ChInd[Channel]].mean()

    # End = perf_counter()-Start
    # print(f'Done in {End}s.')
    LedStart = GetPeaks(abs(np.diff(Ch)))['Pos'][0]/dvInfo['FPS']
    # print('Done.')

    LedVideo.release()
    return(LedStart)


def RGB2BW(FileInput, FileOutput, Codec='same'):
    RGBVideo, FPS = Video.Read(FileInput)

    if str(Codec).lower() == 'same':
        FourCC = int(RGBVideo.get(cv2.CAP_PROP_FOURCC))
    elif str(Codec).lower() == 'auto':
        Ext = FileOutput.split('.')[-1]
        FourCC = Video.GetFourCC(Video.DefaultFourCC[Ext])
    else:
        FourCC = Video.GetFourCC(Codec)

    Dimensions = [int(RGBVideo.get(_)) for _ in [3,4]]

    Output = cv2.VideoWriter(
        filename=FileOutput,
        fourcc=FourCC,
        fps=FPS,
        frameSize=tuple(Dimensions)
    )

    while RGBVideo.isOpened():
        F, Frame = RGBVideo.read()
        if not F: break

        Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        Output.write(Frame)

    RGBVideo.release()
    Output.release()

    return(None)


# Level 1

def Downsample(FileInput, FileOutput, Downsampling, Codec='same'):
    InVideo, FPS = Video.Read(FileInput)

    if str(Codec).lower() == 'same':
        FourCC = int(InVideo.get(cv2.CAP_PROP_FOURCC))
    elif str(Codec).lower() == 'auto':
        Ext = FileOutput.split('.')[-1]
        FourCC = Video.GetFourCC(Video.DefaultFourCC[Ext])
    else:
        FourCC = Video.GetFourCC(Codec)

    Dimensions = [int(InVideo.get(_)/Downsampling) for _ in [3,4]]

    Output = cv2.VideoWriter(
        filename=FileOutput,
        fourcc=FourCC,
        fps=FPS,
        frameSize=tuple(Dimensions)
    )

    while InVideo.isOpened():
        F, Frame = InVideo.read()
        if not F: break

        Frame = FrameScale(Frame, Downsampling)
        Output.write(Frame)

    InVideo.release()
    Output.release()

    return(None)


