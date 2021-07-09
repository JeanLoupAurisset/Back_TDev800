#!/usr/bin/env bash
sshpass -p "$VM_PASS" ssh -o StrictHostKeyChecking=no jl@176.128.78.27 << 'ENDSSH'
 cd /django
 docker login -u $REGISTRY_USER -p $CI_BUILD_TOKEN $CI_REGISTRY
 docker pull registry.gitlab.com/bigshoes/django/djangopg:latest
 docker run --name tdev800 -p 8000:8000 -d djangopg
ENDSSH