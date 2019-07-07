FROM awsdeeplearningteam/mxnet-model-server:1.0.5-mxnet-cpu
COPY featurizer.mar .
CMD ["mxnet-model-server", "--start", "--models", "featurizer=./featurizer.mar", "--model-store", "."]