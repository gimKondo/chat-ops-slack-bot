#!/bin/bash
############################################################
# - param1: AWS CLI's profile name
############################################################
cd `dirname $0`
if [ $# -ne 1 ]; then
  echo "**************** ERROR! require the profile as parameter ****************"
  exit 1
fi
echo "**************** start deploy for ### " $1 " ### ****************"

echo "**************** deleting old archives... ****************"
rm -rf archive/*.zip

func_list=("SlackChatOps")
echo "**************** compressing functions... ****************"
for i in "${func_list[@]}"
do
  zip -j "archive/${i}.zip" "${i}/lambda_function.py"
done

echo "**************** uploading archives... ****************"
for i in "${func_list[@]}"
do
  aws --profile $1 lambda update-function-code --function-name $i --zip-file "fileb://./archive/${i}.zip"
done

if [ $? -gt 0 ]; then
  echo "**************** fail to deploy! ****************"
  exit
fi
echo "**************** complete the deployment! ****************"
