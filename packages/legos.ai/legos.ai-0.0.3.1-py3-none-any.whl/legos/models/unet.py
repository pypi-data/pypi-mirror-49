import torch
import torch.nn.functional as F
from torch import nn
from legos.layers import LayerActivation

class UnetUpBlock(nn.Module):
    def __init__(self, up_channels, res_channels, out_channels):
        super().__init__()

        self.up = nn.ConvTranspose2d(up_channels, out_channels // 2, kernel_size=2, stride=2)
        self.conv = nn.Conv2d(res_channels, out_channels // 2, 1)
        self.bn = nn.BatchNorm2d(out_channels)

    def forward(self, x1, x2):
        """
        x1: previous layer
        x2: residual
        """
        x1 = self.up(x1)
        x2 = self.conv(x2)
        x = torch.cat([x1, x2], dim=1)
        return self.bn(F.relu(x))

class Unet34(nn.Module):
    def __init__(self, base_model):
        super().__init__()

        self.base_model = base_model
        self.base_features = [LayerActivation(base_model[i]) for i in [2, 4, 5, 6]]
        self.up1 = UnetUpBlock(512, 256, 256)
        self.up2 = UnetUpBlock(256, 128, 256)
        self.up3 = UnetUpBlock(256, 64, 256)
        self.up4 = UnetUpBlock(256, 64, 256)
        self.conv_out = nn.ConvTranspose2d(256, 1, 2, stride=2)

    def forward(self, x):
        x = F.relu(self.base_model(x))
        x = self.up1(x, self.base_features[3].features)
        x = self.up2(x, self.base_features[2].features)
        x = self.up3(x, self.base_features[1].features)
        x = self.up4(x, self.base_features[0].features)
        x = self.conv_out(x)

        return x
