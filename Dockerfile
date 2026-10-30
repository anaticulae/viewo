# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

FROM ghcr.io/anaticulae/baw:v1.90.1-python

ENV HOVERPOWER_STORE=/var/workdir/hoverpower/repo

ENV SHARED_SPACE=/var/tmp/space
ENV SHARED_TODO=/var/tmp/space/todo
ENV SHARED_READY=/var/tmp/space/ready
ENV SHARED_TMP=/var/tmp/space/tmp

WORKDIR /var/install

COPY pyproject.toml .

RUN pip install .[dev]
RUN pip install .

COPY . /var/install

RUN pip install .

WORKDIR /var/workdir

ENTRYPOINT ["sh", "-c"]
