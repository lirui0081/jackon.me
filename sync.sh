#!/bin/bash

git pull git@github.com:JackonYang/jackon.me.git master
git submodule update
pelican content

sudo nginx -s reload
