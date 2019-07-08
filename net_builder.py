import mxnet as mx
from mxnet.gluon.model_zoo import vision

if __name__ == "__main__":
    # define the context, use gpu when available
    ctx = mx.gpu() if mx.context.num_gpus() else mx.cpu()
    # load nets from gluon module zoo
    resnet18 = vision.resnet18_v2(pretrained=True, ctx=ctx)
    # get only its featurizer
    resnet18 = resnet18.features
    # call hybridize() to be availble for export
    resnet18.hybridize()
    # do dry run after hybridize() => this is requirements from mxnet
    resnet18(mx.nd.ones((1, 3, 224, 224)))
    # export the nets
    resnet18.export("featurizer")
