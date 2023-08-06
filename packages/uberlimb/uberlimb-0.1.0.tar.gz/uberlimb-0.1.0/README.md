# ÜberLimb

Generative art with CPPN networks.

# Get started

```python
from uberlimb.image import Renderer
from uberlimb.parameters import RendererParams

renderer = Renderer(RendererParams())
frame = renderer.render_frame().as_pillow().show()
```

Expected output:

![](https://cai-misc.s3.eu-central-1.amazonaws.com/uberlimb/uberlimb_splash.png)