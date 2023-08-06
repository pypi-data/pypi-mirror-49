from torch import nn
from legos.layers import UpSampleBlock

class UpSample34(nn.Module):
    """
    UpSampling model with pretrained model as base model.
    """
    def __init__(self, base_model: nn.Module):
        super().__init__()

        self.features = nn.Sequential(
            base_model,
            nn.ReLU(),
            UpSampleBlock(512, 256),
            UpSampleBlock(256, 256),
            UpSampleBlock(256, 256),
            UpSampleBlock(256, 256),
            nn.ConvTranspose2d(256, 1, 2, stride=2)
        )

    def forward(self, x):
        return self.features(x)
