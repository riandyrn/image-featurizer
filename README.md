# Image Featurizer

This project is used to generate image features by using [ResNet18 v2](https://mxnet.incubator.apache.org/api/python/gluon/model_zoo.html).

This project is intended to be used as complementary service for searching similar image like [Thomas Delteil's Visual Search](https://thomasdelteil.github.io/VisualSearch_MXNet/).

The model is served using [MXNet Model Server](https://github.com/awslabs/mxnet-model-server) in Docker.

## Run Service

```bash
> make run
```

This command will execute the service & make it listen to port `8080`.

## Stop Service

```bash
> make stop
```

This command will stop the running service in another terminal.

If we want to stop the service in current terminal simply press `CTRL + C`.

## Test Service

```bash
> make test
```

This command will execute test on service. It will feed the service with `jpeg` image.
