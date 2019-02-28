# Build static files
FROM node:10-stretch-slim as staticfiles

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install node packages and copy webpack configurations
RUN mkdir -p ./main/static
COPY package.json yarn.lock ./
RUN yarn --pure-lockfile

COPY tsconfig.json .
COPY .babelrc .
COPY postcss.config.js .
COPY tailwind.js .
COPY webpack.scripts.config.js .
COPY webpack.styles.config.js .

COPY assets ./assets

RUN yarn build-production


# Actual container
FROM python:3.6-slim-stretch

RUN mkdir -p /usr/share/man/man1
RUN apt update && \
    apt install -y --no-install-recommends \
    curl \
    unzip \
    build-essential \
    openjdk-8-jdk

# Make directory for the app
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/bm3d

# Install bm3d and the matlab runtime
# (NOTE: requires a matlab-compiled installer for the bm3d repo, see readme)
WORKDIR /usr/bm3d
COPY ./noel-bm3d-executable/bm3d.install /usr/bm3d
RUN chmod +x bm3d.install
RUN ./bm3d.install -mode silent -agreeToLicense yes -destinationFolder /usr/bm3d
RUN rm bm3d.install

# Make directory for pip packages
#RUN mkdir -p /usr/lib/pip
#ENV PIP_TARGET /usr/lib/pip

WORKDIR /usr/src/app

# Install python packages
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# Copy app files
COPY ./main ./main
COPY ./noel ./noel
COPY ./manage.py ./manage.py

# Collect staticfiles for nginx to serve them
COPY --from=staticfiles /usr/src/app/main/static ./main/static
RUN python manage.py collectstatic

# Limit privileges and expose port 8001
RUN groupadd -r user && useradd --no-log-init -r -g user user
RUN chown user /usr/src/app -R

ENV BM3D_DIRECTORY /usr/bm3d

CMD python3
