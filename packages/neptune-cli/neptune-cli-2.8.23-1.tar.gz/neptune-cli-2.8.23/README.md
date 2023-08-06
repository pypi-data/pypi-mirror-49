# Neptune client library for Python

## Prerequisites

Install _Git_, _Python_ and _pip_ (eg. using package manager provided with your distribution)

If you are on Debian, you may need to install some packages for numpy:
```bash
  sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
```

Make sure you are logged in to docker-repo.deepsense.codilime.com. Full instruction is available [here](https://codilime.atlassian.net/wiki/display/DM/Private+docker-hub). Repository isn't public, so if you're outside CodiLime network, you need to use VPN.

**Note**: The easiest way to manage required packages is to use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
```bash
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Now you are in separated python environment. To exit, run
```bash
  deactivate
```


## Installation

Obtain archive with neptune - you can either download it from [Artifactory](http://artifactory.deepsense.codilime.com:8081/)
or run
```bash
  make build
```

and install with pip:
```bash
  pip install dist/neptune-cli*.tar.gz
```

Once you have installed the library, you can use Neptune directly from your shell:
```bash
  neptune --help
```


# Using Sentry

To configure Sentry the DSN (Data Source Name) needs to be set.
In order to do this you need to go to
deepsense/neptune/common/sentry.py and change _url.
The DSN tells Sentry where to sent events.

NOTE: It might be worth to consider tying Sentry directly
to Python logging module using SentryHandler.

Details: https://docs.sentry.io/clients/python/integrations/logging/

NOTE: Unfortunately, there is no obvious way to disable console message

      ```
      Sentry is attempting to send 1 pending error messages
      Waiting up to 10 seconds
      ```

      written by Sentry. It is done in a Thread using pure `print`
      without any flags to disable it or queues to join while temporarily
      redirecting stdout. At this moment, the only way I see is monkeypatching.

## Development

#### To clean up swagger binaries, generated code and distribution directory:
```bash
  make clean
```

#### To download and setup dependencies:
```bash
  make prepare
```

#### To generate an API client:
```bash
  make api_client
```

#### To check code style (copyright headers + PEP8):
```bash
  make checkstyle_tests
```

#### To run unit tests:
```bash
  make unit_tests
```

#### To run all tests:
```bash
  make tests
```

#### To create a distribution package:
```bash
  make build
```

#### To publish a snapshot to Artifactory:
```bash
  make publish release=false
```
Make sure you have corrent $HOME/.artifactory_credentials file

#### To publish a release version to Artifactory:
```bash
    make publish release=true
```
Make sure you have corrent $HOME/.artifactory_credentials and $HOME/gerrit_credentials files

#### To run in-docker experiment locally
* add `'--network', 'host'` to `docker_run_command` in `DockerExperimentExecutor`
* `neptune ex run --environment base`

## License

Copyright (c) 2018, deepsense.io

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
