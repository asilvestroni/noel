# noel [![Build Status](https://travis-ci.com/Silver96/noel.svg?branch=master)](https://travis-ci.com/Silver96/noel)
Main repository for the Noise Extraction and User Profile Linking project (NOEL).

This repository contains the code used for a web application based on a research project [[1]](https://www.researchgate.net/publication/326309757_A_Cluster-based_Approach_of_Smartphone_Camera_Fingerprint_for_User_Profiles_Resolution_within_Social_Network) regarding residual noise extraction and smartphone linking, achieved by computing the correlations between each pair of picture noises, which in turn allows for clustering of the given pictures.

## Setup (Docker)
Docker CE and docker-compose are both required for this setup.
A makefile is provided to control docker-compose services.

To ensure a correct startup of all the provided services, one needs to configure the following files.

### config/{key,cert}.pem
Key and Certificate files are required for SSL setup. These can be generated through OpenSSL (`openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem`) or provided through a more sofisticated setup by integrating with certbot. Certbot integration is not currently supported, but should be easy to implement through `certbot/certbot` docker image and edits to the nginx configuration.

### docker/common.env
```bash
cp docker/common.env.example docker/common.env
```
Fill in the required values (refer to the Standalone setup for reference). 
Additionally, generate/type a random string as a value for `DJANGO_SECRET`, since it will be used as a base for Django encryption and hashing.

Django debug mode can be turned off by setting `DJANGO_DEBUG` to `False`.
### config/nginx.conf
A basic nginx config file is provided. Additional setup may be required depending on the context.

## Setup (Standalone)
To simply launch the web app by itself, copy the provided `.env.example` file to `.env`, and fill in the required data.
```bash
# Skips certain steps during session processing; useful for debug
SESSION_SKIP=
# API key for linked Facebook App
FB_API_KEY=

# Redis backend url
REDIS_URL=redis://localhost

# Postgres config
POSTGRES_URL=localhost
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASS=postgress
```
**Note**: in order for the application to function properly, it needs to be served over SSL, since Facebook API only accepts https requests.

## Build Docker Image
To make the provided docker-compose services executable, NOEL's Docker image must be built. This can be achieved by running
```bash
docker build . -f docker/Dockerfile -t <desired-tag>
# or
make docker-build
```
**Note**: to obtain the BM3D executable (required for both standalone setup **AND** Docker build, follow the instructions provided in the submodule's [repository](https://github.com/Silver96/noel-bm3d-executable).
