build:
	-rm featurizer.mar
	model-archiver --model-name featurizer --model-path . --handler featurizer:handle
	docker build -t image-featurizer .

run:
	-make stop
	make build
	docker run -it --rm --name image-featurizer -p 8080:8080 -p 8081:8081 image-featurizer

stop:
	docker stop image-featurizer

install:
	venv/bin/pip install -r requirements.txt

test:
	curl -X POST http://localhost:8080/predictions/featurizer -T dog.jpg