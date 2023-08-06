import numpy as np
from PIL import Image

from uberlimb.input_space import InputSpace
from uberlimb.model.limb_model import LimbModel
from uberlimb.parameters import RendererParams, FrameColorMap


class LimbFrame:
    def __init__(self, arr: np.ndarray):
        self._raw_arr = arr
        self.arr = arr

    def as_pillow(self) -> Image:
        img = Image.fromarray(self.arr.astype(np.uint8))
        return img

    def as_array(self):
        return self.arr

    def postprocess_normed(self, dither_strength: float):
        raise NotImplementedError

    def postprocess_binning(self, dither_strength: float):
        arr = self._raw_arr.ravel()
        arr = arr + (np.random.random(arr.size) - 0.5) * (dither_strength / 256)
        splits = np.array_split(np.sort(arr), 510)
        cutoffs = [x[-1] for x in splits][:-1]
        discrete = np.digitize(arr, cutoffs, right=True)
        arr = discrete.reshape(*self._raw_arr.shape)
        arr = np.abs(255 - arr % 510)
        arr = arr.astype(np.uint8)
        self.arr = arr


class Renderer:
    def __init__(self, params: RendererParams):
        self._params = params
        self.model = LimbModel.get_model(self._params.model)
        self.input_space = InputSpace(self._params.input)

    def render_frame(self) -> LimbFrame:
        # TODO set batch size based on params count
        arr = self.model.predict(self.input_space.arr, batch_size=int(2 ** 18))
        arr = arr.reshape(self._params.input.y_resolution,
                          self._params.input.x_resolution,
                          3)
        frame = LimbFrame(arr)
        if self._params.post_fx.color_map == FrameColorMap.BINNING:
            frame.postprocess_binning(self._params.post_fx.dither_strength)
        elif self._params.post_fx.color_map == FrameColorMap.NORMED:
            frame.postprocess_normed(self._params.post_fx.dither_strength)
        return frame
