#!/usr/bin/env bash
ssh -o StrictHostKeyChecking=no root@176.128.78.27 << 'ENDSSH'
 cd /your_project_name
 docker login -u $REGISTRY_USER -p $CI_BUILD_TOKEN $CI_REGISTRY
 docker pull registry.gitlab.com/bigshoes/django:latest
 docker-compose up -d
ENDSSH
