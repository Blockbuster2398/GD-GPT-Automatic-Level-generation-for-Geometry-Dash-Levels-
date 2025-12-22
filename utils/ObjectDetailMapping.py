class ObjectMapping:
    attribute_to_key = {}
    key_to_attribute = {}
    def __init__(self):
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
            "unknown_31" : 31, # Almost certainly text field for "A" block
            "scale": 32,
            "unknown_54" : 54, # Something to do with teleport portals
            "groups": 57,  # See Google Doc ("Period-separated list (e.g., 1.2.10)")
            "editor_layer_two": 61,
            "dont_fade": 64,
            "dont_enter": 67,
            "unknown155": 155, # Appears frequently in Nine Circles
            "unknown156": 156,  # Appears frequently in Nine Circles
            # Specific to Triggers
            "trigger_red": 7,
            "trigger_green": 8,
            "trigger_blue": 9,
            "trigger_duration": 10,
            "trigger_touch": 11,
            "trigger_checked": 13,
            "tint_ground": 14, # Added after
            "trigger_player_one": 15,
            "trigger_player_two": 16,
            "trigger_blending": 17,
            "trigger_target_color": 23,
            "trigger_x_movement": 28,
            "trigger_y_movement": 29,
            "trigger_easing_id": 30,
            "trigger_opacity": 35,
            "unknown36": 36, # Always 1, for some unknown reason. (No clue what this does)
            "unknown_45": 45,  # Has some role in the functionality of toggle triggers
            "trigger_target_group_id": 51,
            "trigger_center_group_id": 52,
            "unknown_56": 56,  # Has some role in the functionality of toggle triggers
            "trigger_pickup_id" : 80,
            "trigger_multi_trigger": 87,
            "unknown_128": 128, # Has some role in the functionality of toggle triggers
            "unknown_129": 129  # Has some role in the functionality of toggle triggers
        }
        self.key_to_attribute = {value: key for key, value in self.attribute_to_key.items()}
        print(self.attribute_to_key)
        print(self.key_to_attribute)