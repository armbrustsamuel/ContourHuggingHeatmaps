import torch

import torch.nn as nn
import segmentation_models_pytorch as smp
from matplotlib import pyplot as plt


class Unet(nn.Module):
    def __init__(self, cfg_model, no_of_landmarks):
        super(Unet, self).__init__()
        self.unet = smp.Unet(
            encoder_name=cfg_model.ENCODER_NAME,
            encoder_weights=cfg_model.ENCODER_WEIGHTS,
            decoder_channels=cfg_model.DECODER_CHANNELS,
            in_channels=cfg_model.IN_CHANNELS,
            classes=no_of_landmarks,
        )
        self.temperatures = nn.Parameter(torch.ones(1, no_of_landmarks, 1, 1), requires_grad=False)

    def forward(self, x):
        print(x.shape)
        print(x)
        plt.imshow(x[0,0])
        plt.show()
        return self.unet(x)

    def scale(self, x):
        y = x / self.temperatures
        print("X")
        # print(x)
        print(x.shape)
        plt.imshow(x[0,0])
        plt.show()

        print("Y")
        # print(y)
        print(y.shape)
        plt.imshow(y[0,0])
        plt.show()

        # compare = torch.eq(x, y)
        # print(compare)

        print("Temperatures")
        print(self.temperatures.shape)
        # print(self.temperatures)
        # plt.imshow(self.temperatures)
        # plt.show() 

        # x=torch.Tensor(compare)
        # print("testing transpose")
        # print(np.transpose(np.argwhere(x==False)))

        return y


def two_d_softmax(x):
    exp_y = torch.exp(x)
    return exp_y / torch.sum(exp_y, dim=(2, 3), keepdim=True)


def nll_across_batch(output, target):
    nll = -target * torch.log(output.double())
    return torch.mean(torch.sum(nll, dim=(2, 3)))
