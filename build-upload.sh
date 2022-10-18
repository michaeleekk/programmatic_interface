version=$1
docker build -t biomage/programmatic-interface:${version} .

docker login
docker push biomage/programmatic-interface:${version}
