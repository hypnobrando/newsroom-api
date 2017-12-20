#!/bin/bash

if [ $1 != "production" ] ;
then
  echo env must be production
  exit
fi

ecr_login="$(aws ecr get-login)"
str_to_rm=" -e none"
eval "$(echo "$ecr_login" | sed "s@$str_to_rm@@")"

docker build -t newsroom-api:$1 .;
docker tag newsroom-api:$1 832531170141.dkr.ecr.us-east-2.amazonaws.com/newsroom-api:$1;

docker push 832531170141.dkr.ecr.us-east-2.amazonaws.com/newsroom-api:$1;

~/src/ecs-deploy/./ecs-deploy -c bep-projects -n newsroom-api -i 832531170141.dkr.ecr.us-east-2.amazonaws.com/newsroom-api:$1;
