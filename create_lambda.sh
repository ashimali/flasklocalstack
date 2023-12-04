#!/bin/bash

cd lambdas
pip install requests -t .
zip -r ../function.zip .
cd -

awslocal lambda create-function \
    --function-name test-lambda \
    --runtime python3.10 \
    --role arn:aws:iam::000000000000:role/execution_role \
    --handler lambda.handler \
    --zip-file fileb://function.zip \
    --region eu-west-2


awslocal lambda create-event-source-mapping \
    --function-name test-lambda \
    --event-source-arn arn:aws:sqs:eu-west-2:000000000000:test-queue
