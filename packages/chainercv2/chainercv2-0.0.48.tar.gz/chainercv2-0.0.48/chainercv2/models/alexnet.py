"""
    AlexNet for ImageNet-1K, implemented in Chainer.
    Original paper: 'One weird trick for parallelizing convolutional neural networks,'
    https://arxiv.org/abs/1404.5997.
"""

__all__ = ['AlexNet', 'alexnet']

import os
import chainer.functions as F
import chainer.links as L
from chainer import Chain
from functools import partial
from chainer.serializers import load_npz
from .common import SimpleSequential


class AlexConv(Chain):
    """
    AlexNet specific convolution block.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    ksize : int or tuple/list of 2 int
        Convolution window size.
    stride : int or tuple/list of 2 int
        Stride of the convolution.
    pad : int or tuple/list of 2 int
        Padding value for convolution layer.
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 ksize,
                 stride,
                 pad):
        super(AlexConv, self).__init__()
        with self.init_scope():
            self.conv = L.Convolution2D(
                in_channels=in_channels,
                out_channels=out_channels,
                ksize=ksize,
                stride=stride,
                pad=pad,
                nobias=False)
            self.activ = F.relu

    def __call__(self, x):
        x = self.conv(x)
        x = self.activ(x)
        return x


class AlexDense(Chain):
    """
    AlexNet specific dense block.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    """

    def __init__(self,
                 in_channels,
                 out_channels):
        super(AlexDense, self).__init__()
        with self.init_scope():
            self.fc = L.Linear(
                in_size=in_channels,
                out_size=out_channels)
            self.activ = F.relu
            self.dropout = partial(
                F.dropout,
                ratio=0.5)

    def __call__(self, x):
        x = self.fc(x)
        x = self.activ(x)
        x = self.dropout(x)
        return x


class AlexOutputBlock(Chain):
    """
    AlexNet specific output block.

    Parameters:
    ----------
    in_channels : int
        Number of input channels.
    classes : int
        Number of classification classes.
    """
    def __init__(self,
                 in_channels,
                 classes):
        super(AlexOutputBlock, self).__init__()
        mid_channels = 4096

        with self.init_scope():
            self.fc1 = AlexDense(
                in_channels=in_channels,
                out_channels=mid_channels)
            self.fc2 = AlexDense(
                in_channels=mid_channels,
                out_channels=mid_channels)
            self.fc3 = L.Linear(
                in_size=mid_channels,
                out_size=classes)

    def __call__(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x


class AlexNet(Chain):
    """
    AlexNet model from 'One weird trick for parallelizing convolutional neural networks,'
    https://arxiv.org/abs/1404.5997.

    Parameters:
    ----------
    channels : list of list of int
        Number of output channels for each unit.
    ksizes : list of list of int
        Convolution window sizes for each unit.
    strides : list of list of int or tuple/list of 2 int
        Strides of the convolution for each unit.
    pads : list of list of int or tuple/list of 2 int
        Padding value for convolution layer for each unit.
    in_channels : int, default 3
        Number of input channels.
    in_size : tuple of two ints, default (224, 224)
        Spatial size of the expected input image.
    classes : int, default 1000
        Number of classification classes.
    """
    def __init__(self,
                 channels,
                 ksizes,
                 strides,
                 pads,
                 in_channels=3,
                 in_size=(224, 224),
                 classes=1000):
        super(AlexNet, self).__init__()
        self.in_size = in_size
        self.classes = classes

        with self.init_scope():
            self.features = SimpleSequential()
            with self.features.init_scope():
                for i, channels_per_stage in enumerate(channels):
                    stage = SimpleSequential()
                    with stage.init_scope():
                        for j, out_channels in enumerate(channels_per_stage):
                            setattr(stage, "unit{}".format(j + 1), AlexConv(
                                in_channels=in_channels,
                                out_channels=out_channels,
                                ksize=ksizes[i][j],
                                stride=strides[i][j],
                                pad=pads[i][j]))
                            in_channels = out_channels
                        setattr(stage, "pool{}".format(i + 1), partial(
                            F.max_pooling_2d,
                            ksize=3,
                            stride=2,
                            pad=0))
                    setattr(self.features, "stage{}".format(i + 1), stage)

            in_channels = in_channels * 6 * 6
            self.output = SimpleSequential()
            with self.output.init_scope():
                setattr(self.output, 'flatten', partial(
                    F.reshape,
                    shape=(-1, in_channels)))
                setattr(self.output, 'classifier', AlexOutputBlock(
                    in_channels=in_channels,
                    classes=classes))

    def __call__(self, x):
        x = self.features(x)
        x = self.output(x)
        return x


def get_alexnet(model_name=None,
                pretrained=False,
                root=os.path.join("~", ".chainer", "models"),
                **kwargs):
    """
    Create AlexNet model with specific parameters.

    Parameters:
    ----------
    model_name : str or None, default None
        Model name for loading pretrained model.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.chainer/models'
        Location for keeping the model parameters.
    """
    channels = [[64], [192], [384, 256, 256]]
    ksizes = [[11], [5], [3, 3, 3]]
    strides = [[4], [1], [1, 1, 1]]
    pads = [[2], [2], [1, 1, 1]]

    net = AlexNet(
        channels=channels,
        ksizes=ksizes,
        strides=strides,
        pads=pads,
        **kwargs)

    if pretrained:
        if (model_name is None) or (not model_name):
            raise ValueError("Parameter `model_name` should be properly initialized for loading pretrained model.")
        from .model_store import get_model_file
        load_npz(
            file=get_model_file(
                model_name=model_name,
                local_model_store_dir_path=root),
            obj=net)

    return net


def alexnet(**kwargs):
    """
    AlexNet model from 'One weird trick for parallelizing convolutional neural networks,'
    https://arxiv.org/abs/1404.5997.

    Parameters:
    ----------
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.chainer/models'
        Location for keeping the model parameters.
    """
    return get_alexnet(model_name="alexnet", **kwargs)


def _test():
    import numpy as np
    import chainer

    chainer.global_config.train = False

    pretrained = False

    models = [
        alexnet,
    ]

    for model in models:
        net = model(pretrained=pretrained)
        weight_count = net.count_params()
        print("m={}, {}".format(model.__name__, weight_count))
        assert (model != alexnet or weight_count == 61100840)

        x = np.zeros((1, 3, 224, 224), np.float32)
        y = net(x)
        assert (y.shape == (1, 1000))


if __name__ == "__main__":
    _test()
