### Description

This repo contains the script to build the python dependencies inside the amazon linux container for lambda function. 
It creates the .zip deployment file which can be uploaded to lambda console to create a function.

##### Why we need to build the dependencies inside the container? 
AWS uses their own aws base images in lambda function which is based on amazon linux distribution, 
so sometime when you build a package in your machine (macos, windows or any other linux distribution) might not 
compatable with native aws linux os distribution. 

This might lead into some import error while executing the function. For example following error will occur when you
use google cloud pypi package, because aws linux uses different build path compared other operating system 
for cython related modules

```bash
cannot import name 'cygrpc' from 'grpc._cython' (/var/task/grpc/_cython/__init__.py)
```

#### How to solve?

Build .zip deployment file inside the amazon native container, Here the makefile script contains the set of instructions
which will create a python virtual env and install the pypi dependencies and zip it. 

```csv
make run
```

