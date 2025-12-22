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
            "editor_layer_one": 20,
            "color_one_id": 21,
            "color_two_id": 22,
            "z_layer": 24,
            "z_order": 25,
            "scale": 32,
            "groups": 57,  # See Google Doc ("Period-separated list (e.g., 1.2.10)")
            "editor_layer_two": 61,
            "dont_fade": 64,
            "dont_enter": 67,
            # Specific to Triggers
            "trigger_red": 7,
            "trigger_green": 8,
            "trigger_blue": 9,
            "trigger_duration": 10,
            "trigger_touch": 11,
            "trigger_checked": 13,
            "trigger_player_one": 15,
            "trigger_player_two": 16,
            "trigger_blending": 17,
            "trigger_target_color": 23,
            "trigger_x_movement": 28,
            "trigger_y_movement": 29,
            "trigger_easing_id": 30,
            "trigger_opacity": 35,
            "trigger_target_group_id": 51,
            "trigger_center_group_id": 52,
            "trigger_pickup_id" : 80,
            "trigger_multi_trigger": 87
        }
        self.key_to_attribute = {value: key for key, value in self.attribute_to_key.items()}
        print(self.attribute_to_key)
        print(self.key_to_attribute)