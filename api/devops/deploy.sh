#!/usr/bin/env bash
ssh -o StrictHostKeyChecking=no jl@176.128.78.27 << 'ENDSSH'
 cd /your_project_name
 docker login -u $REGISTRY_USER -p $CI_BUILD_TOKEN $CI_REGISTRY
 docker pull registry.gitlab.com/BigShoes/django/djangopg:latest
 docker run --name api -p 8000:8000 -d djangopg
ENDSSH
