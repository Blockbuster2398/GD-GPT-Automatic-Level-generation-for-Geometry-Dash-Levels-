class ObjectMap:
    attribute_to_key = {}
    key_to_attribute = {}
    category_to_id = {}

    def __init__(self):
        # Where booleans are applicable, 0 = false and 1 = true
        # Sets default values for an object
        self.attribute_to_key = {
            "object_type": 999,  # Custom, implemented by me
            "object_id": 1,
            "x_position": 2,
            "y_position": 3,
            "flip_horizontal": 4,
            "flip_vertical": 5,
            "rotation": 6,
            "unknown_19": 19,  # Something to do with the sideways path guide arrow
            "editor_layer_one": 20,
            "color_one_id": 21,
            "color_two_id": 22,
            "z_layer": 24,
            "z_order": 25,
            "unknown_31": 31,  # Almost certainly text field for "A" block
            "scale": 32,
            "unknown41": 41,  # No clue, related to a one-sided-block outline?
            "unknown43": 43,  # No clue, related to a one-sided-block outline?
            "unknown_54": 54,  # Something to do with teleport portals
            "groups": 57,  # See Google Doc ("Period-separated list (e.g., 1.2.10)")
            "editor_layer_two": 61,
            "dont_fade": 64,
            "dont_enter": 67,
            "unknown155": 155,  # Appears frequently in Nine Circles
            "unknown156": 156,  # Appears frequently in Nine Circles
            # Specific to Triggers
            "trigger_red": 7,
            "trigger_green": 8,
            "trigger_blue": 9,
            "trigger_duration": 10,
            "trigger_touch": 11,
            "trigger_checked": 13,
            "tint_ground": 14,  # Added after
            "trigger_player_one": 15,
            "trigger_player_two": 16,
            "trigger_blending": 17,
            "trigger_target_color": 23,
            "trigger_x_movement": 28,
            "trigger_y_movement": 29,
            "trigger_easing_id": 30,
            "trigger_opacity": 35,
            "unknown36": 36,  # Always 1, for some unknown reason. (No clue what this does)

            "unknown_45": 45,  # Has some role in the functionality of toggle triggers
            "trigger_target_group_id": 51,
            "trigger_center_group_id": 52,
            "unknown_56": 56,  # Has some role in the functionality of toggle triggers
            "unknown_58": 58,  # Related to Move trigger
            "unknown_68": 68,  # Related to Rotate trigger
            "unknown_69": 69,  # Related to Rotate trigger
            "unknown_70": 70,  # Related to Rotate trigger
            "unknown_71": 71,  # Related to Rotate trigger
            "unknown_85": 85,  # Related to Rotate trigger
            "trigger_pickup_id": 80,
            "trigger_multi_trigger": 87,
            "unknown_128": 128,  # Has some role in the functionality of toggle triggers
            "unknown_129": 129  # Has some role in the functionality of toggle triggers
        }
        self.key_to_attribute = {value: key for key, value in self.attribute_to_key.items()}

        self.category_to_id = {

            # Orbs (dx, dy)
            "green_orb" : [1022],
            "red_orb" : [1333],  # Exclude???
            "black_orb" : [1330],
            "purple_orb" : [141],
            "yellow_orb" : [36],
            "blue_orb" : [84],

            # Pads (dx, dy, rotation*)
            "red_pad" : [1332],
            "yellow_pad" : [35],
            "blue_pad" : [67],
            "purple_pad" : [140],

            # Portals (dx, dy)

            "blue_gravity" : [10],
            "yellow_gravity" : [11],
            "cube_portal" : [12],
            "ship_portal" : [13],
            "ball_portal" : [47],
            "ufo_portal" : [111],
            "wave_portal" : [660],
            "robot_portal" : [745],
            "spider_portal" : [1331],

            "teleport_portal" : [747],

            "green_size" : [99],
            "pink_size" : [101],

            "start_dual" : [287],
            "end_dual" : [286],

            "orange_reflect" : [46],
            "blue_reflect" : [46],

            "xhalf_speed" : [200],
            "x1_speed" : [201],
            "x2_speed" : [202],
            "x3_speed" : [203],
            "x4_speed" : [1334],  # Exclude???

            # Blocks (dx, dy) and (dx, dy, hFlip)
            "full_block" : [1, 2, 3, 4, 6, 7, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 90, 91, 92, 93, 95, 96, 116,
                          117, 118, 119, 121, 122, 146, 147, 160, 162, 165, 166, 168, 169, 173, 175, 207, 208, 209, 210,
                          212, 213, 250, 152, 253, 255, 256, 257, 258, 260, 261, 263, 264, 265, 267, 268, 269, 271, 272,
                          270, 274, 275, 467, 469, 470, 471, 472, 473, 474],
            "half_block" : [40, 62, 63, 64, 65, 66, 68, 147, 170, 171, 172, 174, 192, 215, 369, 370, 664, 663, 662],
            "mini_block" : [176, 194, 195, 196, 197, 204, 206, 219, 220, 661],

            # Spikes (dx, dy, flip*)
            "spike" : [8, 144, 149, 177, 216],
            "spike_short" : [9, 61, 39, 135, 178, 205, 217, 243, 244, 265, 368, 421, 422, 446, 447, 719],
            "spike_mini" : [103, 145, 179, 218, 392, 459, 1156, 1155, 1157, 1122],

            # Saws (dx, dy)
            "saw_mini" : [98, 188, 185, 399, 680, 677, 742, 1707, 1736],
            "saw_med" : [89, 187, 184, 398, 679, 676, 741, 1620, 1709, 1706, 1735],
            "saw_large" : [88, 186, 183, 397, 675, 678, 740, 1619, 1708, 1705, 1734],

            # Slopes (dx, dy, flip*) and (dx, dy, flip*, and rotation)
            "slope" : [289, 294, 299, 309, 305, 309, 315, 321, 326, 331, 337, 343, 349, 343, 371, 483, 492, 665, 673, 711,
                     728, 726],
            "slope_long" : [291, 295, 301, 307, 311, 317, 323, 327, 333, 339, 345, 351, 355, 372, 484, 493, 666, 674, 712,
                          729, 727]

        }

        self.category_to_id_create = {
            # Orbs (dx, dy)
            "green_orb": 1022,
            "red_orb": 1333,  # Exclude???
            "black_orb": 1330,
            "purple_orb": 141,
            "yellow_orb": 36,
            "blue_orb": 84,
            # Pads (dx, dy, rotation*)
            "red_pad": 1332,
            "yellow_pad": 35,
            "blue_pad": 67,
            "purple_pad": 140,
            # Portals (dx, dy)
            "blue_gravity": 10,
            "yellow_gravity": 11,
            "cube_portal": 12,
            "ship_portal": 13,
            "ball_portal": 47,
            "ufo_portal": 111,
            "wave_portal": 660,
            "robot_portal": 745,
            "spider_portal": 1331,
            "teleport_portal": 747,
            "green_size": 99,
            "pink_size": 101,
            "start_dual": 287,
            "end_dual": 286,
            "orange_reflect": 46,
            "blue_reflect": 46,
            "xhalf_speed": 200,
            "x1_speed": 201,
            "x2_speed": 202,
            "x3_speed": 203,
            "x4_speed": 1334,  # Exclude???
            # Blocks (dx, dy) and (dx, dy, hFlip)
            "full_block": 83,
            "half_block": 40,
            "mini_block": 195,
            # Spikes (dx, dy, flip*)
            "spike": 8,
            "spike_short": 39,
            "spike_mini": 103,
            # Saws (dx, dy)
            "saw_mini": 98,
            "saw_med": 89,
            "saw_large": 88,
            # Slopes (dx, dy, flip*) and (dx, dy, flip*, and rotation)
            "slope": 289,
            "slope_long": 291,

            "_": 396
        }



        # Avoid creating variations of tokens based on dx and dy, as changes in position will be encoded by their own tokens

