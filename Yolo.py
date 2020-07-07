import os, sys
import pandas as pd
import numpy as np

from keras_yolo3.yolo import YOLO 
from Utils import make_dirname, get_dirname
from Image import open_image

src_dir = get_dirname(0)
keras_dir = make_dirname(src_dir, "keras_yolo3")

CONFIG = {
    "model_path": make_dirname(src_dir, "model_weights", "trained_weights_final.h5"),
    "anchors_path": make_dirname(keras_dir, "model_data", "yolo_anchors.txt"),
    "classes_path": make_dirname(src_dir, "model_weights", "data_classes.txt"),
    "score": 0.25,
    "gpu_num": 1,
    "model_image_size": (416, 416),
}

OUT_COLS = [
    "image",
    "image_path",
    "xmin",
    "ymin",
    "xmax",
    "ymax",
    "label",
    "confidence",
    "x_size",
    "y_size",
]

class Yolo():
    def __init__(self):
        # Yolo setup
        self.yolo = YOLO(
            **{
                "model_path": CONFIG["model_path"],
                "anchors_path": CONFIG["anchors_path"],
                "classes_path": CONFIG["classes_path"],
                "score": CONFIG["score"],
                "gpu_num": CONFIG["gpu_num"],
                "model_image_size": (416, 416),
            }
        )

        # Make a dataframe for the prediction outputs
        self.out_df = pd.DataFrame(
            columns=OUT_COLS
        )

    def predict(self, img_path, out_dir):
        class_file = open(CONFIG["classes_path"], "r")
        input_labels = [line.rstrip("\n") for line in class_file.readlines()]

        self.out_df = pd.DataFrame(
            columns=OUT_COLS
        )

        total = len(os.listdir(img_path))
        for i, filename in enumerate(os.listdir(img_path)):
            print("\rDetecting image ", i, " of ", total, end="", flush=True)
            image = open_image(os.path.join(img_path, filename))
            prediction, predict_image = self.yolo.detect_image(image)
            y_size, x_size, _ = np.array(predict_image).shape

            for single_prediction in prediction:
                self.out_df = self.out_df.append(
                    pd.DataFrame(
                        [
                            [
                                filename,
                                img_path.rstrip("\n"),
                            ]
                            + single_prediction
                            + [x_size, y_size]
                        ],
                        columns=OUT_COLS,
                    )
                )

        self.out_df.to_csv(out_dir, index=False)
    