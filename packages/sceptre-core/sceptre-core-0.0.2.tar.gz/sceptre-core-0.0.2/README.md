# Sceptre

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=bugs)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=coverage)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=alert_status)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=security_rating)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=sqale_index)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Sceptre_sceptre-core&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=Sceptre_sceptre-core)
![image](https://circleci.com/gh/Sceptre/sceptre-core.png?style=shield)

# About

Sceptre is a tool to drive
[AWS CloudFormation](https://aws.amazon.com/cloudformation). It automates the
mundane, repetitive and error-prone tasks, enabling you to concentrate on
building better infrastructure.

# Install

`$ pip install sceptre-core`

More information on installing sceptre can be found in our
[Installation Guide](https://sceptre.cloudreach.com/latest/docs/install.html)

# Example

Sceptre organises Stacks into "Stack Groups". Each Stack is represented by a
YAML configuration file stored in a directory which represents the Stack Group.
Here, we have two Stacks, `vpc` and `subnets`, in a Stack Group named `dev`:

```
$ tree
.
├── config
│   └── dev
│        ├── config.yaml
│        ├── subnets.yaml
│        └── vpc.yaml
└── templates
    ├── subnets.py
    └── vpc.py
```

## Usage

Sceptre can be used from the CLI (see `sceptre-cli`), or imported as a Python
package.

## Python API

Using Sceptre as a Python module is very straightforward. You need to create a
SceptreContext, which tells Sceptre where your project path is and which path
you want to execute on, we call this the "command path".

After you have created a SceptreContext you need to pass this into a
SceptrePlan. On instantiation the SceptrePlan will handle all the required steps
to make sure the action you wish to take on the command path are resolved.

After you have instantiated a SceptrePlan you can access all the actions you can
take on a Stack, such as `validate()`, `launch()`, `list()` and `delete()`.

```python
from sceptre.context import SceptreContext
from sceptre.plan.plan import SceptrePlan

context = SceptreContext("/path/to/project", "command_path")
plan = SceptrePlan(context)
plan.launch()
```

Full API reference documentation can be found in the
[Documentation](https://sceptre.cloudreach.com/)

# Use Docker Image

View our [Docker repository](https://hub.docker.com/r/cloudreach/sceptre-core).

To use our Docker image follow these instructions:

1. Pull the image `docker pull cloudreach/sceptre-core:[SCEPTRE_VERSION_NUMBER]`
   e.g. `docker pull cloudreach/sceptre-core:x.x.x`. Leave out the version
   number if you wish to run `latest` or run
   `docker pull cloudreach/sceptre-core:latest`.

2. Run the image. You will need to mount the working directory where your
   project resides to a directory called `project`. You will also need to mount
   a volume with your AWS config to your docker container. E.g.

If you want to use a custom ENTRYPOINT simply amend the Docker command:

`docker run -ti --entrypoint='' cloudreach/sceptre-core:latest sh`

The above command will enter you into the shell of the Docker container where
you can execute sceptre commands - useful for development.

If you have any other environment variables in your non-docker shell you will
need to pass these in on the Docker CLI using the `-e` flag. See Docker
documentation on how to achieve this.

## Tutorial and Documentation

- [Get Started](https://sceptre.cloudreach.com/latest/docs/get_started.html)
- [Documentation](https://sceptre.cloudreach.com/)

## Contributing

See our [Contributing Guide](CONTRIBUTING.md)
