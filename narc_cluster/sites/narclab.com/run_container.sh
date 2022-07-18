IMAGE=narclabcom:v1.0.3

docker service create -p 3000:3000 --name narclabcom ${IMAGE}