# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import join

from pytest import fixture

import viewo
from viewo.job import FILE_NAME
from viewo.job import JobInfo
from viewo.job import common_folder
from viewo.job import dump
from viewo.job import load
from viewo.upload import free_todo


def test_dump_and_load(tmpdir):
    """Dump and load project an example configuration"""
    config = JobInfo(
        title='Name',
        date='Date',
        result='Result',
        index=1337,
    )

    path = join(tmpdir, 'configuration.yaml')
    dump(path, config)
    loaded = load(path)

    assert loaded == config


@fixture
def common(tmpdir):
    """Create common folder with `todo` and `ready` folder. Todo contains 3
    elements, ready 2."""
    todo = join(tmpdir, 'todo')
    ready = join(tmpdir, 'ready')
    makedirs(todo)
    makedirs(ready)

    for item in [1234, 5555, 4321]:
        folder = join(todo, '%d' % item)
        makedirs(folder)
        output = join(folder, FILE_NAME)
        result = JobInfo('Super Duper Masterarbeit', '2019.04.01', None, item)
        dump(output, result)

    for item in [3333, 5555]:
        folder = join(ready, '%d' % item)
        makedirs(folder)
        output = join(folder, FILE_NAME)
        result = JobInfo('Super Masterarbeit', '2019.04.05', '95%', item)
        dump(output, result)

    makedirs(join(todo, 'broken'))
    makedirs(join(ready, 'also_broken'))

    return tmpdir


def test_common_folder(common):
    jobs = common_folder(common)
    assert len(jobs[0] + jobs[1]) == 5, str(jobs)


def test_free_todo(tmpdir, monkeypatch):
    """Generate the same random name twice. This happens not very often, but
    it can happen."""

    folder = iter(['test', 'test', 'ts'])

    def random_foldername():
        return next(folder)

    def todo():
        return tmpdir

    with monkeypatch.context() as context:
        context.setattr(viewo.upload, 'random_foldername', random_foldername)
        context.setattr(viewo.upload, 'todo', todo)

        # Create folder name, so the next call is already created
        makedirs(join(tmpdir, free_todo()))

        # test is already there, give me the next one
        assert free_todo() == 'ts'
