# -*- coding: utf-8 -*-
from .base_image import IMAGE
import cv2
name = 'base_image'


def create(img=None, flags=cv2.IMREAD_COLOR, path=''):
    return IMAGE(img, flags, path)