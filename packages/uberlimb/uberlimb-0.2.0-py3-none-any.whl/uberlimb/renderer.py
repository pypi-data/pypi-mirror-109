from uberlimb.frame import LimbFrame
from uberlimb.input_space import InputSpace
from uberlimb.model.model import LimbModel
from uberlimb.parameters import RendererParams, FrameColorMap


class Renderer:
    def __init__(self, params: RendererParams):
        self.params = params
        self.model = LimbModel.build_model(self.params.model)
        self.input_space = InputSpace(self.params.input)

    def update_model(self):
        self.model = LimbModel.build_model(self.params.model)

    def update_input_space(self):
        self.input_space = InputSpace(self.params.input)

    def render_frame(self) -> LimbFrame:
        # TODO set batch size based on params count
        arr = self.model.predict(self.input_space.arr, batch_size=int(2 ** 18))
        arr = arr.reshape(self.params.input.y_resolution,
                          self.params.input.x_resolution,
                          3)
        frame = LimbFrame(arr)
        if self.params.post_fx.color_map == FrameColorMap.BINNING:
            frame.postprocess_binning(self.params.post_fx.dither_strength)
        elif self.params.post_fx.color_map == FrameColorMap.NORMED:
            frame.postprocess_normed(self.params.post_fx.dither_strength)
        return frame
