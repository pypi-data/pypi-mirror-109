import numpy as np
from pydantic import validate_arguments

from uberlimb.parameters import InputSpaceParams


class InputSpace:
    @validate_arguments
    def __init__(self, params: InputSpaceParams):
        self.arr = self._create_input_array(params)

    @staticmethod
    @validate_arguments
    def _create_input_array(params: InputSpaceParams) -> np.ndarray:
        SIZE_CONSTANT = 1920
        # basic init
        x = params.x_resolution * params.scale / SIZE_CONSTANT
        x = np.linspace(-x, x, params.x_resolution)
        y = params.y_resolution * params.scale / SIZE_CONSTANT
        y = np.linspace(-y, y, params.y_resolution)
        # offset
        if params.offset_x:
            x_offset = x.ptp() * params.offset_x / x.size
            x += x_offset
        if params.offset_y:
            y_offset = y.ptp() * params.offset_y / y.size
            y += y_offset

        x, y = np.meshgrid(x, y)
        # rotation
        if params.rotation:
            rot = params.rotation * np.pi / 180
            x_rot = np.cos(rot) * x + np.sin(rot) * y
            y_rot = np.cos(rot + np.pi / 2) * x + np.sin(rot + np.pi / 2) * y
            x, y = x_rot, y_rot

        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        # custom function
        if params.custom_fuction:
            f = eval(params.custom_fuction)
        else:
            f = np.sqrt(x ** 2 + y ** 2)

        alpha = np.full((x.size, 1), params.alpha)
        beta = np.full((x.size, 1), params.beta)
        z = np.full((x.size, 1), 0)
        input_space = x, y, z, alpha, beta, f
        input_space = np.concatenate(np.array(input_space), axis=1)
        return input_space
