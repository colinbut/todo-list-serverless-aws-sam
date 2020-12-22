#!/bin/bash
aws s3 rb s3://todo-list-archive-bucket-cb --force
aws cloudformation delete-stack --stack-name todo-list-serverless