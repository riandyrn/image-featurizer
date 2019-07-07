import json
from typing import List

import mxnet as mx
import numpy as np

from mxnet_model_service import MXNetModelService


# transform is used for transforming `input_image` into
# format which suitable to neural network used in the inference
def transform(input_image: mx.nd.NDArray) -> mx.nd.NDArray:
    # we need to transform the input image resolution to 224x224,
    # we are doing this by setting the shortest length to 224 then
    # crop the image in center using window which has width of 224
    resized = mx.image.resize_short(input_image, 224)
    cropped, _ = mx.image.center_crop(resized, (224, 224))

    # now we need to normalize the image, to do it we first convert
    # the pixel value into 0..1 then do normalization using settings
    # specified in:
    #
    # https://mxnet.incubator.apache.org/api/python/gluon/model_zoo.html
    cropped = cropped.astype(np.float32) / 255
    normalized: mx.nd.NDArray = mx.image.color_normalize(cropped,
                                                         mean=mx.nd.array([0.485, 0.456, 0.406]),
                                                         std=mx.nd.array([0.229, 0.224, 0.225]))

    # the current dimension of normalized image is (H, W, C), yet what
    # we need is (C, H, W) so we need to transpose the image data
    transposed: mx.nd.NDArray = normalized.transpose((2, 0, 1))

    # we need to add one more dimension to make the dimension (N, C, H, W)
    return transposed.expand_dims(axis=0)


class Featurizer(MXNetModelService):

    def preprocess(self, batch: List):
        if len(batch) == 0:
            return None

        result = []
        for i in range(0, len(batch)):
            # get request
            request: dict = batch[i]

            # try to get the image data from request
            param_name = self.signature['inputs'][0]['data_name']
            data = request.get(param_name)
            if data is None:
                data = request.get("body")
            if data is None:
                data = request.get("data")

            # if data still None, just return immediately
            if data is None:
                return None

            # convert image data (bytearray) to NDArray using
            # utility function given by mxnet
            img: mx.nd.NDArray = mx.image.imdecode(data)

            # transform the array to suitable format for neural
            # network used for inference
            img = transform(img)

            # append the transformed image to result
            result.append(img)

        return result

    def postprocess(self, inference_output: List[mx.nd.NDArray]):
        # load categories
        categories = np.array(json.load(open('image_net_labels.json', 'r')))

        result = []
        for i in range(0, len(inference_output)):
            # convert to inference_output to probabilities
            # using softmax() function
            probabilities: mx.nd.NDArray = inference_output[i].softmax()

            # get top probabilities
            top_probabilities = probabilities.topk(k=3)[0].asnumpy()

            # prepare result
            predictions = []
            for index in top_probabilities:
                predictions.append({
                    "category": categories[int(index)],
                    # we cannot access directly the value on mx.nd.NDArray,
                    # to do that we need to call .asscalar()
                    "probability": probabilities[0][int(index)].asscalar() * 100
                })

            # append predictions to result
            result.append(predictions)

        return result
