#!/usr/bin/bash
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

FILE="env/Production"
TMP="tmp"
VIEWO=$(baw info stable)
DESCRIBE=$(baw info describe)
TAG="${CAELUM_DOCKER_TEST}/release_view:${DESCRIBE}"
echo "baw image create --name ${TAG} --dockerfile ${TMP}"
# insert current viewo version
sed "s/CURRENT/${VIEWO}/" ${FILE} > ${TMP}
baw image create --name $TAG --dockerfile ${TMP}
if [ $? -ne 0 ]
then
    echo "could not run docker build: ${FILE}"
    exit 1
fi
# reset dockerfile
rm ${TMP}
