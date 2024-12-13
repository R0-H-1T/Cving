import cv2
import os
from PIL import Image
from seaborn import heatmap
import pandas as pd
from ultralytics import YOLO
from ultralytics.engine.results import Results, Probs, Boxes
from typing import Union
from pathlib import Path
import shutil


def organize(directory_path: Union[str, Path]):
    model = YOLO(model="yolo11n.pt")

    # Train the model on coco8 dataset
    # results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

    # Needs major rework -->
    try:
        my_dirs = set()
        results: Results = model(source=directory_path)

        for res in results:
            if res.summary():
                print("somethign", res.path)
                org_class = res.summary()[0].get("name")
                print("ORG LABEL::", org_class)
                try:
                    if org_class not in my_dirs and not os.path.isdir(
                        f"{directory_path}/{org_class}"
                    ):
                        os.mkdir(path=f"{directory_path}/{org_class}")

                    _, filename = os.path.split(res.path)
                    shutil.move(
                        src=res.path, dst=f"{directory_path}/{org_class}/{filename}"
                    )
                    my_dirs.add(org_class)
                    print("SRC ", f"{directory_path}/{org_class}")
                    print("DESTL ", f"{directory_path}/{org_class}/{filename}")

                except FileExistsError:
                    raise

                except Exception:
                    raise

    except FileNotFoundError:
        print("File Not Found")


if __name__ == "__main__":
    organize(directory_path="C:/Users/rohit/Documents/test_imgs")
