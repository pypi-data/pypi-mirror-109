from skud_point.main import SkudPoint


class GPhotocell(SkudPoint):
    def __init__(self, point_number, skud_sdk, *args, **kwargs):
        super().__init__(skud_sdk, point_number, *args, **kwargs)
