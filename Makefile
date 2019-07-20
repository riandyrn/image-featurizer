build:
	-rm featurizer.mar
	make build-nets
	model-archiver --model-name featurizer --model-path . --handler featurizer:handle --force
	docker build -t image-featurizer .

run:
	-make stop
	make build
	docker run -it --rm --name image-featurizer -p 8080:8080 -p 8081:8081 image-featurizer

run-service:
	make build
	docker run -d -it --restart=always --name image-featurizer -p 8080:8080 -p 8081:8081 image-featurizer

stop:
	docker stop image-featurizer

install:
	venv/bin/pip install -r requirements.txt

test:
	curl -X POST http://localhost:8080/predictions/featurizer -T dog.jpg
	#curl -X POST http://localhost:8080/predictions/featurizer -T kitten.jpg
	#curl -X POST http://localhost:8080/predictions/featurizer -T kitten-2.jpg

# used to build the neural nets then export it to file
build-nets:
	venv/bin/python net_builder.py

docker-push:
	make build
	docker tag image-featurizer riandyrn/image-featurizer:1.0.0
	docker push riandyrn/image-featurizer:1.0.0