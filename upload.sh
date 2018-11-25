#!/bin/bash
export AWS_SECRET_ACCESS_KEY=mysecret
export AWS_ACCESS_KEY_ID=mykey
export AWS_BUCKET=mybucket

echo "/data/bin/s3-uploader -path=$1 -bucket=$AWS_BUCKET --uploadto=$1" 
/data/bin/s3-uploader -path=$1 -bucket=$AWS_BUCKET --uploadto=$1
