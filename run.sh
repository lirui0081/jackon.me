#!/bin/bash

pelican content
cd output
python -m SimpleHTTPServer
