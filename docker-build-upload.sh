version=$1
docker build -t biomage/programmatic-interface:${version} .

docker login -u biomage
docker push biomage/programmatic-interface:${version}
