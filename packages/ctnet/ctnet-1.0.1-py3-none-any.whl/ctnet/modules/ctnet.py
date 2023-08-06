from torch import nn
import numpy as np


class CTBlockLatent(nn.Sequential):
    def __init__(self, in_array, out_features=200):
        super(CTBlockLatent, self).__init__()
        latent = np.prod(in_array)
        self.activ = nn.LeakyReLU()
        self.dense_1 = nn.Linear(in_features=latent, out_features=out_features)
        # self.dp_1 = nn.Dropout(0.2)
        self.dense_2 = nn.Linear(in_features=out_features, out_features=latent)

        # self.dp_2 = nn.Dropout(0.2)

    def forward(self, x):
        x_shape = x.shape
        x = x.reshape(x.shape[0], 1, -1)
        x = self.dense_1(x)
        x = self.activ(x)

        # x = x.reshape(x_shape)

        x = self.dense_2(x)
        x = self.activ(x)


        x = x.reshape(x_shape)


        return x

class CTBlockInv(nn.Sequential):
    def __init__(self, filters):
        super(CTBlockInv, self).__init__()
        self.conv = nn.ConvTranspose3d(in_channels=filters[0],
                                       out_channels=filters[1],
                                       kernel_size=4,
                                       padding=1,
                                       stride=2)
        # nn.init.xavier_uniform_(self.conv.weight)
        self.activation = nn.LeakyReLU()
        self.batchnorm = nn.BatchNorm3d(filters[1])
        # self.dropout = nn.Dropout3d(0.2)

    def forward(self, x):
        x = self.conv(x)
        x = self.activation(x)
        x = self.batchnorm(x)
        # x = self.dropout(x)
        return x

class CTBlock(nn.Sequential):
    def __init__(self, filters):
        super(CTBlock, self).__init__()
        self.conv = nn.Conv3d(in_channels=filters[0],
                              out_channels=filters[1],
                              kernel_size=4,
                              stride=2,
                              padding=1)
        # nn.init.xavier_uniform_(self.conv.weight)
        self.activation = nn.LeakyReLU()
        self.batchnorm = nn.BatchNorm3d(filters[1])
        # self.dropout = nn.Dropout3d(0.2)

    def forward(self, x):
        x = self.conv(x)
        x = self.activation(x)
        x = self.batchnorm(x)
        # x = self.dropout(x)
        return x

class CTNet(nn.Module):
    def __init__(self,
                 dim=64,
                 id="ctnet",
                 input_mean=None):
        super(CTNet, self).__init__()
        """ 

        :param params:
        :param hvd:
        """
        self.dim =dim
        self.id=id
        # Network parameters
        self.input_mean = np.array(np.load(input_mean), dtype=np.float32) if input_mean is not None else None
        self.encoder = nn.Sequential(
            CTBlock(filters=[1, 64]),
            CTBlock(filters=[64, 128]),
            CTBlock(filters=[128, 256]),
            CTBlock(filters=[256, 512]),

        )

        self.code = CTBlockLatent([512, dim//16, dim//16, dim//16])

        self.decoder = nn.Sequential(
            CTBlockInv(filters=[512, 256]),
            CTBlockInv(filters=[256, 128]),
            CTBlockInv(filters=[128, 64]),
            CTBlockInv(filters=[64, 1]),

        )

    def forward(self, x):
        x = x.reshape(x.shape[0], 1, x.shape[1], x.shape[2], x.shape[3])
        x = self.encoder(x)

        x = self.code(x)

        x = self.decoder(x)
        x = nn.Sigmoid()(x)
        x = x.reshape(x.shape[0], x.shape[2], x.shape[3], x.shape[4])
        return x
