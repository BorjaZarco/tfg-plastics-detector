
import sys
import numpy as np
import pandas as pd
import random

import os
from Utils import make_dir, clear_dir, get_dirname, make_dirname
from Image import split_image, rebuild_image
from Yolo import Yolo

def detect():
    src_dir = get_dirname(0)

    in_dir = make_dirname(src_dir, "in")

    tmp_dir = make_dirname(src_dir, "tmp")
    # tmp_csv_dir = make_dirname(tmp_dir, "csv")

    out_dir = make_dirname(src_dir, "out")
    out_img_dir = make_dirname(out_dir, "images")

    make_dir(tmp_dir)

    for filename in os.listdir(in_dir):
        tmp_split = make_dirname(tmp_dir, filename.split(".")[0], "images")
        make_dir(tmp_split)
        split_image(in_dir, filename, tmp_split)

    yolo3_dir = make_dirname(src_dir, "keras_yolo3")
    
    detector = Yolo()
    for dirname in os.listdir(tmp_dir):
        img_dir = make_dirname(tmp_dir, dirname, 'images')
        make_dir(make_dirname(tmp_dir, dirname, 'csv'))
        csv_dir = make_dirname(tmp_dir, dirname, 'csv', dirname + '.csv')
        detector.predict(img_dir, csv_dir)

    class_file = open(make_dirname(src_dir, "model_weights", "data_classes.txt"), "r")
    classes = [line.rstrip("\n") for line in class_file.readlines()]

    for img_name in os.listdir(tmp_dir):
        # img_name = img_folder.split(".")[0]
        img_file = [filename for filename in os.listdir(in_dir) if img_name in filename][0]

        img_file = make_dirname(in_dir, img_file)
        csv_file = make_dirname(tmp_dir, img_name, 'csv', img_name + ".csv")

        make_dir(make_dirname(out_dir, img_name, 'csv'))
        make_dir(make_dirname(out_dir, img_name, 'images'))

        out_img = make_dirname(out_dir, img_name, "images", "result_" + img_name + ".jpg")
        out_csv = make_dirname(out_dir, img_name, "csv", "result_" + img_name + ".csv")
        rebuild_image(img_file, csv_file, out_img, out_csv, classes)

    clear_dir(tmp_dir)

if __name__ == "__main__":
    if 'detect' in sys.argv:
        detect()