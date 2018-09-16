#! /bin/bash

docker-compose -f docker-compose.yaml -f docker-compose-tests.yaml up --build --exit-code-from end_to_end_tests
