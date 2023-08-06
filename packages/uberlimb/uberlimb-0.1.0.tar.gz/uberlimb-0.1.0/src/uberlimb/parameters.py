from enum import Enum
from typing import Optional

from pydantic import (BaseModel, PositiveInt, PositiveFloat, conint, Field)

from uberlimb.model.models_impl import ModelArchitecture


class ModelActivation(str, Enum):
    SIGMOID = 'sigmoid'
    TANH = 'tanh'


class ModelParams(BaseModel):
    seed: int = 42
    width: PositiveInt = 3
    depth: PositiveInt = 3
    variance: PositiveFloat = 512
    architecture: ModelArchitecture = ModelArchitecture.DENSENET
    activation: ModelActivation = ModelActivation.SIGMOID


class InputSpaceParams(BaseModel):
    alpha: float = 0.5
    beta: float = 0.5
    scale: PositiveFloat = 1
    offset_x: float = 0
    offset_y: float = 0
    custom_fuction: Optional[str] = None
    x_resolution: conint(gt=1, multiple_of=2) = 1280
    y_resolution: conint(gt=1, multiple_of=2) = 800
    rotation: float = 0
    resolution_factor: PositiveFloat = 1


class FrameColorMap(str, Enum):
    BINNING = 'binning'
    NORMED = 'normed'


class PostFXParams(BaseModel):
    dither_strength: float = 2
    color_map: FrameColorMap = FrameColorMap.BINNING


class RendererParams(BaseModel):
    model: ModelParams = Field(default_factory=ModelParams)
    input: InputSpaceParams = Field(default_factory=InputSpaceParams)
    post_fx: PostFXParams = Field(default_factory=PostFXParams)
