FROM awsdeeplearningteam/mxnet-model-server:1.0.7-mxnet-cpu
COPY config.properties .
COPY featurizer.mar .
CMD ["mxnet-model-server", "--start", "--models", "featurizer=./featurizer.mar", "--model-store", "."]