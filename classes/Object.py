from utils.ObjectMapping import ObjectMap
class GMD_Object:

    def __init__(self):
        self.details = {
            # Inherent to all objects
            "object_type" : None, # Custom, implemented by me
            "object_id" : None,
            "x_position" : None, # Change to None?
            "y_position" : None, # Change to None?
            "flip_horizontal" : 0, # False,
            "flip_vertical" : 0, # False,
            "rotation" : 0,
            "unknown_19": 19,  # Something to do with the sideways path guide arrow
            "editor_layer_one" : 0,
            "color_one_id": None,
            "color_two_id" : None,
            "z_layer" : 0,
            "z_order" : 0,
            "unknown_31": None,  # Almost certainly text field for "A" block,
            "scale" : 1,
            "unknown41": 41,  # No clue, related to a one-sided-block outline
            "unknown43": 43,  # No clue, related to a one-sided-block outline
            "unknown_54": None,  # Something to do with teleport portals
            "groups" : None, # See Google Doc ("Period-separated list (e.g., 1.2.10)")
            "editor_layer_two" : 0,
            "dont_fade" : None,
            "dont_enter" : None,
            "unknown155": None, # Appears frequently in Nine Circles
            "unknown156": 156,  # Appears frequently in Nine Circles
            # Specific to Triggers
            "trigger_red" : None,
            "trigger_green" : None,
            "trigger_blue" : None,
            "trigger_duration" : None,
            "trigger_touch" : None,
            "trigger_checked" : None,
            "tint_ground": None,
            "trigger_player_one" : None,
            "trigger_player_two" : None,
            "trigger_blending" : None,
            "trigger_target_color" : None,
            "trigger_x_movement" : None,
            "trigger_y_movement" : None,
            "trigger_easing_id" : None,
            "trigger_opacity" : None,
            "unknown36": None,  # Always 1, for some unknown reason. (No clue what this does)
            "unknown_45": None,  # Has some role in the functionality of toggle triggers
            "trigger_target_group_id" : None,
            "trigger_center_group_id" : None,
            "unknown_56": None,  # Has some role in the functionality of toggle triggers
            "unknown_58": None,  # Related to Move trigger
            "unknown_68": None,  # Related to Rotate trigger
            "unknown_69": None,  # Related to Rotate trigger
            "unknown_70": None,  # Related to Rotate trigger
            "unknown_71": None,  # Related to Rotate trigger
            "unknown_85": None,  # Related to Rotate trigger
            "trigger_pickup_id" : None,
            "trigger_multi_trigger" : None,
            "unknown_128": None, # Has some role in the functionality of toggle triggers
            "unknown_129": None, # Has some role in the functionality of toggle triggers

            # Special Details
            "x_distance": None,
            "y_distance": None
        }
        self.sequence_order = None # 0 indexed order of object in level placement
        self.map = ObjectMap()
        self.category = None
    def to_gmd_format(self):
        object_string = ""
        for key in self.details.keys():
            if self.details[key] != None:
                # object_string += (str(key) + str(self.details[key]) + ",")
                object_string += (str(self.map.attribute_to_key[str(key)]) + "," + str(self.details[key]) + ",")
        object_string = object_string[:-1]
        return object_string


    def __str__(self):
        return (
                "Sequence order: " + str(self.sequence_order) +
                ", GMD_Object ID: " + str(self.details["object_id"]) +
                ", X: " + str(self.details["x_position"]) +
                ", Y: " + str(self.details["y_position"]) +
                ", X_distance: " + str(self.details["x_distance"]) +
                ", Y_distance: " + str(self.details["y_distance"]))

        return (
                "Sequence order: " + str(self.sequence_order) +
                ", GMD_Object ID: " + str(self.details["object_id"]) +
                ", X: " + str(self.details["x_position"]) +
                ", Y: " + str(self.details["y_position"]))

object = GMD_Object()
object.to_gmd_format()