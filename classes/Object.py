class GMD_Object:
    details = {
        # Inherent to all objects
        "object_type" : None, # Custom, implemented by me
        "object_id" : None,
        "x_position" : None, # Change to None?
        "y_position" : None, # Change to None?
        "flip_horizontal" : False,
        "flip_vertical" : False,
        "rotation" : 0,
        "editor_layer_one" : 0,
        "color_one_id": None,
        "color_two_id" : None,
        "z_layer" : 0,
        "z_order" : 0,
        "scale" : 1,
        "groups" : "", # See Google Doc ("Period-separated list (e.g., 1.2.10)")
        "editor_layer_two" : 0,
        "dont_fade" : None,
        "dont_enter" : None,
        # Specific to Triggers
        "trigger_red" : None,
        "trigger_green" : None,
        "trigger_blue" : None,
        "trigger_duration" : None,
        "trigger_touch" : None,
        "trigger_checked" : None,
        "trigger_player_one" : None,
        "trigger_player_two" : None,
        "trigger_blending" : None,
        "trigger_target_color" : None,
        "trigger_x_movement" : None,
        "trigger_y_movement" : None,
        "trigger_easing_id" : None,
        "trigger_opacity" : None,
        "trigger_target_group_id" : None,
        "trigger_center_group_id" : None,
        "trigger_pickup_id" : None,
        "trigger_multi_trigger" : None
    }

    def __init__(self):
        return
    """def __init__(self, objectID, xPosition, yPosition, hFlip, vFlip, rotation):
        # Simple Constructor
        self.details = {
            "object_type": "",  # Custom, implemented by me
            "object_id": objectID,
            "x_position": xPosition,
            "y_position": yPosition,
            "flip_horizontal": hFlip,
            "flip_vertical": vFlip,
            "rotation": rotation,
        }"""

    """def __init__(self, objectID, xPosition, yPosition):
        self.object_id = objectID
        self.x_position = xPosition
        self.y_position = yPosition"""

    def __str__(self):
        return (
                "GMD_Object ID: " + str(self.details["object_id"]) +
                " X: " + str(self.details["x_position"]) +
                " Y: " + str(self.details["y_position"]))
