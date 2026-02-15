from classes.Level import GMD_Level
from pathlib import Path
from collections import defaultdict
from utils.ObjectMapping import ObjectMap


# level = GMD_Level("input_levels/color_test.gmd")

# level = GMD_Level("input_levels/nine_circles.gmd")
# print(level)
# print(level.tokens)
# level.create_gmd("output_levels/ten_circles.gmd", "ten_circles", "(10/10)")
with open("./resources/data_tokenized.txt", "r") as f:
    objects = GMD_Level.decode_tokens(f.read())
    # print(objects)

    level_reconstructed = GMD_Level("_", objects)
    # level_reconstructed.create_gmd("output_levels/square10.gmd", "squares", "???")
    print(f"Level reconstructed: {level_reconstructed}")


    level = GMD_Level("input_levels/the spanish flee.gmd")
    print(f"Level: {level}")

# TODO fix level off by one error
"""Sequence order: 0, GMD_Object ID: 747, X: 0, Y: 0, X_distance: None, Y_distance: None
Sequence order: 1, GMD_Object ID: 396, X: 60, Y: 270, X_distance: 60, Y_distance: 270
Sequence order: 2, GMD_Object ID: 396, X: 120, Y: 300, X_distance: 60, Y_distance: 30
Sequence order: 3, GMD_Object ID: 396, X: 180, Y: 330, X_distance: 60, Y_distance: 30
Sequence order: 4, GMD_Object ID: 396, X: 240, Y: 360, X_distance: 60, Y_distance: 30
Sequence order: 5, GMD_Object ID: 83, X: 315, Y: 0, X_distance: 75, Y_distance: -360
Sequence order: 6, GMD_Object ID: 83, X: 375, Y: 0, X_distance: 60, Y_distance: 0
Sequence order: 7, GMD_Object ID: 83, X: 435, Y: 0, X_distance: 60, Y_distance: 0
Sequence order: 8, GMD_Object ID: 83, X: 465, Y: 0, X_distance: 30, Y_distance: 0
Sequence order: 9, GMD_Object ID: 83, X: 495, Y: 0, X_distance: 30, Y_distance: 0
Sequence order: 10, GMD_Object ID: 140, X: 495, Y: 17, X_distance: 0, Y_distance: 17
Sequence order: 11, GMD_Object ID: 203, X: 495, Y: 30, X_distance: 0, Y_distance: 13
Sequence order: 12, GMD_Object ID: 141, X: 615, Y: 60, X_distance: 120, Y_distance: 30
Sequence order: 13, GMD_Object ID: 141, X: 675, Y: 90, X_distance: 60, Y_distance: 30
Sequence order: 14, GMD_Object ID: 141, X: 735, Y: 120, X_distance: 60, Y_distance: 30
Sequence order: 15, GMD_Object ID: 36, X: 825, Y: 150, X_distance: 90, Y_distance: 30
Sequence order: 16, GMD_Object ID: 13, X: 915, Y: 240, X_distance: 90, Y_distance: 90
Sequence order: 17, GMD_Object ID: 1022, X: 945, Y: 240, X_distance: 30, Y_distance: 0
Sequence order: 18, GMD_Object ID: 1022, X: 1035, Y: 0, X_distance: 90, Y_distance: -240
Sequence order: 19, GMD_Object ID: 1330, X: 1155, Y: 90, X_distance: 120, Y_distance: 90
Sequence order: 20, GMD_Object ID: 36, X: 1215, Y: 0, X_distance: 60, Y_distance: -90
Sequence order: 21, GMD_Object ID: 84, X: 1425, Y: 150, X_distance: 210, Y_distance: 150
Sequence order: 22, GMD_Object ID: 47, X: 1725, Y: 0, X_distance: 300, Y_distance: -150
Sequence order: 23, GMD_Object ID: 1022, X: 1815, Y: 0, X_distance: 90, Y_distance: 0
Sequence order: 24, GMD_Object ID: 1022, X: 1875, Y: 60, X_distance: 60, Y_distance: 60
Sequence order: 25, GMD_Object ID: 1022, X: 1935, Y: 0, X_distance: 60, Y_distance: -60
Sequence order: 26, GMD_Object ID: 83, X: 2115, Y: 30, X_distance: 180, Y_distance: 30
Sequence order: 27, GMD_Object ID: 83, X: 2145, Y: 30, X_distance: 30, Y_distance: 0
Sequence order: 28, GMD_Object ID: 83, X: 2175, Y: 30, X_distance: 30, Y_distance: 0
Sequence order: 29, GMD_Object ID: 83, X: 2175, Y: 120, X_distance: 0, Y_distance: 90
Sequence order: 30, GMD_Object ID: 83, X: 2205, Y: 120, X_distance: 30, Y_distance: 0"""