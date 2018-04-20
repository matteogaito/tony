#!/bin/bash

DOCKER_NAME="matteogaito/tony"

GITCMD="$(which git)"
MD5SUM="$(which md5sum; if [ $? -ne 0 ]; then which md5; fi)"
PROJDIR="$( cd "$(dirname "$0")" ; pwd -P )"
CODEDIR="${PROJDIR}/code"
ARCHITECTURE=$(uname -m)
git pull

VERSION="$(tar -c --exclude "*.git" ${PROJDIR} | ${MD5SUM} | cut -d" " -f1)"

CHECKEXIST="$(docker images | grep $DOCKER_NAME | grep -c $VERSION )"

if [ $CHECKEXIST -eq 0 ]
then
	cd $PROJDIR

	for i in $(docker ps -a | grep tony | awk '{ print $1 }');
	do
		echo "Stopping docker $i"
		docker stop $i
		docker rm $i
	done

	docker build -t ${DOCKER_NAME}:${VERSION} -f Dockerfile-${ARCHITECTURE} .
	docker run -d -p 5000:5000 -v ${CODEDIR}:/tony ${DOCKER_NAME}:${VERSION}
else
	echo "Version already built"
	docker images | grep $VERSION
fi

