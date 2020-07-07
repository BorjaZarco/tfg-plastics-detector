import os
import pandas as pd

from collections import namedtuple
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax label acc')
color_dict = ["green", "blue", "red", "yellow", "black", "orange", "pink"]
OUT_COLS = [
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

def split_image(src_dir, filename, out_dir):
    grid_image = open_image(os.path.join(src_dir, filename))
    grid_width, grid_height = grid_image.size

    overlap = 170
    
    for h in range(1, int(grid_height/overlap) - 1):
        for w in range(1, int(grid_width/overlap) - 1):
            left = overlap * (w - 1)
            right = left + (overlap * 3)
            top = overlap * (h - 1)
            bot = top + (overlap * 3)
            
            crop_img = grid_image.crop((left, top, right, bot))

            crop_img.save(os.path.join(out_dir, "grid_" + str(top) + "_" + str(left) + ".jpg"))

def rebuild_image(img_file, csv_file, out_img, out_csv, classes, treshold=0.5):
    detect_csv = pd.read_csv(csv_file)
    out_df = pd.DataFrame(
        columns=OUT_COLS
    )
    total_rectangles = [generate_rectangles(row) for _, row in detect_csv.iterrows()]
    grid_image = Image.open(os.path.join(img_file))
    
    rectangles = []
    
    for i, rect1 in enumerate(total_rectangles):
        j = 0
        if rect1.acc < treshold: 
            continue
        while j < len(total_rectangles):
            if j == i: 
                j += 1
                continue
            rect2 = total_rectangles[j]
            intersection = intersection_percentage(rect1, rect2)
            if intersection > 0.25 and rect1.acc <= rect2.acc:
                break
            j += 1

        if j == len(total_rectangles):
            rectangles.append(rect1)
            out_df = out_df.append(
                pd.DataFrame(
                    [
                        [
                            out_img,
                            rect1.xmin,
                            rect1.ymin,
                            rect1.xmax,
                            rect1.ymax,
                            rect1.label,
                            rect1.acc,
                            rect1.xmax - rect1.xmin, 
                            rect1.ymax - rect1.ymin
                        ]
                    ],
                    columns=OUT_COLS
                )
            )

    out_df.to_csv(out_csv, index=False)
    print("Rectangles: ", str(len(rectangles)))
    print("Total Rectangles: ", str(len(total_rectangles)))
    paint_rectangles(rectangles, grid_image, out_img, classes)

def paint_rectangles(rectangles, grid_image, out_img, classes):
    draw = ImageDraw.Draw(grid_image)

    for rect in rectangles:
        draw.rectangle([(rect.xmin, rect.ymin), (rect.xmax, rect.ymax)], outline=color_dict[rect.label])
        draw.text((rect.xmin, rect.ymin - 10), "" + str(classes[rect.label]) + ": " + str(rect.acc), fill=color_dict[rect.label])

    grid_image.save(out_img)


def generate_rectangles(csv_row):
    filename = csv_row["image"].split(".")[0]
    [_, h_offset, w_offset] = filename.split("_")
    xmin = int(w_offset) + int(csv_row["xmin"])
    xmax = int(w_offset) + int(csv_row["xmax"])

    ymin = int(h_offset) + int(csv_row["ymin"])
    ymax = int(h_offset) + int(csv_row["ymax"])

    return Rectangle(xmin, ymin, xmax, ymax, int(csv_row["label"]), float(csv_row["confidence"]))


def intersection_percentage(rect1, rect2):
    ia = intersection_area(rect1, rect2)
    if (ia != None and ia > 0.0):
        rect1_area = (rect1.xmax - rect1.xmin) * (rect1.ymax - rect1.ymin)
        rect2_area = (rect2.xmax - rect2.xmin) * (rect2.ymax - rect2.ymin)
        percentage = ia / (rect1_area + rect2_area - ia)
        
        return percentage if percentage != None else 0
    else:
        return 0

# returns None if rectangles don't intersect
def intersection_area(rect1, rect2):  
    dx = min(rect1.xmax, rect2.xmax) - max(rect1.xmin, rect2.xmin)
    dy = min(rect1.ymax, rect2.ymax) - max(rect1.ymin, rect2.ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy
    else:
        return 0 

def open_image(img_path):
    try:
        image = Image.open(img_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        return image
    except:
        print("File Open Error! Try again!")
        return None, None