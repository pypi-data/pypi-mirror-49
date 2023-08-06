# Fixture File Handler

This project helps you to vacate specific file path or deploy resource file into specific file path when unit testing.

## Context

The most popular setup / teardown tasks about file system on unit testing is
almost 2 kinds.

1. vacate specific file path for testing file export function 
2. deploy fixture file into specific file path for testing file import function

Then we have to think about how to back up existing file between unit testing
because maybe developer wants to keep those handwritten file for development.

`Fixture File Handler` is framework to realize simply implement
the vacate and deploy actions while keeping the existing files.
Of course, even if there is no file in the target path, it works fine.

## Ubiquitous Language

### target

The target file path to vacate or deploy file for unit testing.

### backup

The file path to back up existing file on target file path between unit testing.

### resource

The file you want to deploy and let product code read in unit testing.
It may test resource file or template file like `*.dist` file.

## Basic behavior

### Vacator

target path|backup path
---|---
existing file|&nbsp;

↓ setup

target path|backup path
---|---
&nbsp;|existing file

↓ teardown

target path|backup path
---|---
existing file|&nbsp;


### Deployer

target path|backup path|resource path
---|---|---
existing file|&nbsp;|resource file

↓ setup

target path|backup path|resource path
---|---|---
resource file|existing file|resource file

↓ teardown

target path|backup path|resource path
---|---|---
existing file|&nbsp;|resource file


### Common behavior

If file or directory already exists on backup path,
setup raise `BackupAlreadyExistError`
because it's unexpected situation and developer may want to resque its backup file.

## Quickstart

#### 1. Install
`pip install fixturefilehandler`

#### 2-1. Case when unittest: implement setUp() and doCleanups()

```python
from pathlib import Path
import unittest

from fixturefilehandler.factories import VacatorFactory
from fixturefilehandler.file_paths import RelativeVacateFilePath

VACATOR = VacatorFactory.create(
    RelativeVacateFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path(__file__).parent
    )
)


class ConfigurableTestCase(unittest.TestCase):
    def setUp(self):
        VACATOR.setup()

    def doCleanups(self):
        VACATOR.teardown()
```

#### 2-2. Case when pytest: implement fixture

```python
from pathlib import Path
import pytest

from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import RelativeDeployFilePath

DEPLOYER = DeployerFactory.create(
    RelativeDeployFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path('testresources/test.txt.dist'),
        Path(__file__).parent
    )
)


@pytest.fixture
def fixture_file():
    DEPLOYER.setup()
    yield DEPLOYER.FILE_PATH
    DEPLOYER.teardown()


def test_something(fixture_file):
    """test something"""
```

## API

### file_paths

#### SimpleVacateFilePath

This instance holds path to target and backup.
Each path is independent each other.

#### SimpleDeployFilePath

This instance holds path to target, backup, and resource.
Each path is independent each other.

#### RelativeVacateFilePath

This instance holds path to target, backup, and base.
Each path is relative based on base path.

#### RelativeDeployFilePath

This instance holds path to target, backup, resource, and base.
Each path is relative based on base path.

## How do I...

### Use different paths for each test?

`setup()` and `teardown()` also accept file_paths argument.

Case when unittest:

```python
from pathlib import Path

import unittest

from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.file_paths import RelativeDeployFilePath


class AdvancedConfigurableTestCase(unittest.TestCase):
    @property
    def file_path(self) -> RelativeDeployFilePath:
        return RelativeDeployFilePath(
            Path('test.txt'),
            Path('test.txt.bak'),
            Path(f'testresources/{self._testMethodName}.txt'),
            Path(__file__).parent
        )

    def setUp(self):
        ResourceFileDeployer.setup(self.file_path)

    def doCleanups(self):
        ResourceFileDeployer.teardown(self.file_path)
```

Case when pytest:

```python
from pathlib import Path

import pytest

from fixturefilehandler import ResourceFileDeployer
from fixturefilehandler.file_paths import RelativeDeployFilePath


@pytest.fixture
def fixture_file_advanced(request):
    file_path = RelativeDeployFilePath(
        Path('test.txt'),
        Path('test.txt.bak'),
        Path(f'testresources/{request.node.name}.txt'),
        Path(__file__).parent
    )

    ResourceFileDeployer.setup(file_path)
    yield file_path
    ResourceFileDeployer.teardown(file_path)


def test_something(fixture_file_advanced):
    """test something"""
```