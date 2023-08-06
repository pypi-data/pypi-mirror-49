![opsworks-cli](src/opsworks-cli.png)

opsworks-cli
======================

A simple python module to work with aws opsworks.

[![Build Status](https://travis-ci.org/chaturanga50/opsworks-cli.svg?branch=master)](https://travis-ci.org/chaturanga50/opsworks-cli) [![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=chaturanga50_opsworks-cli&metric=alert_status)](https://sonarcloud.io/dashboard?id=chaturanga50_opsworks-cli)
[![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=chaturanga50_opsworks-cli&metric=coverage)](https://sonarcloud.io/component_measures/metric/coverage/list?id=chaturanga50_opsworks-cli)
[![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=chaturanga50_opsworks-cli&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=chaturanga50_opsworks-cli)
[![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=chaturanga50_opsworks-cli&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=chaturanga50_opsworks-cli) [![PyPI version](https://badge.fury.io/py/opsworks-cli.svg)](https://badge.fury.io/py/opsworks-cli) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

How to install
--------------

You can download the updated release version from pypi repo using `pip` or directly from our github [releases](https://github.com/chaturanga50/opsworks-cli/releases) and `unzip` the content.

``` bash
pip install opsworks-cli
```

Configuration
--------------

`opsworks-cli` needs to access the AWS API using your credentials. Just like the AWS SDK or CLI, it will look for credentials in two places:

- From the shared credentials file (~/.aws/credentials)
- From environment variables

To use the credentials file, create a `~/.aws/credentials` file based on the template below:

``` bash
[default]
aws_access_key_id=your_access_key
aws_secret_access_key=your_secret_key
```

Usage
-----

You can see the list of parameters available via `opsworks-cli --help`

Options:

- [Update custom cookbook](#update-custom-cookbook) - Update all the cookbook cache in the instances in the layer or update all the instances in entire stack.
- [Execute recipes](#execute-recipes) - Execute specific cookbook against layer or stack.
- [Setup](#setup) - Running setup against layer or stack.
- [Deploy](#deploy) - Deploy application to the layer or stack.

update-custom-cookbook
----------------------

```bash
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (optional)
```

```bash
opsworks-cli update-custom-cookbooks --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e
```

```bash
opsworks-cli update-custom-cookbooks --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0
```

execute-recipes
---------------

```bash
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (optional)
* cookbook - chef cookbook (required)
* custom-json - custom json file with extra vars (optional)
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --cookbook apache::default \
             --custom-json [{"lamp":{ "packages": { "app-sso": "17.1.6" } } }]
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --cookbook apache::default
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --cookbook apache::default
             --custom-json [{"lamp":{ "packages": { "app-sso": "17.1.6" } } }]
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --cookbook apache::default
```

setup
-----

```bash
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (optional)
```

```bash
opsworks-cli setup --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e
```

```bash
opsworks-cli setup --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0
```

deploy
------

```bash
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (optional)
* app - OpsWorks application ID (required)
* custom-json - custom json file with extra vars (optional)
```

```bash
opsworks-cli deploy --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --app 2da891ea-1809-480d-a799-cb2c08746115 \
             --custom-json [{"lamp":{ "packages": { "app-sso": "17.1.6" } } }]
```

```bash
opsworks-cli deploy --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --app 2da891ea-1809-480d-a799-cb2c08746115 \
             --custom-json [{"lamp":{ "packages": { "app-sso": "17.1.6" } } }]
```

```bash
opsworks-cli deploy --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --app 2da891ea-1809-480d-a799-cb2c08746115
```

```bash
opsworks-cli deploy --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --app 2da891ea-1809-480d-a799-cb2c08746115
```

How it works
------------

- sending opsworks commands via aws api to specific stack or layer id.
- then `opsworks-cli` is waiting for the response output from aws api.
- once we got the response from aws api, `opsworks-cli` will show the final output accordingly.

Contributing
------------

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

Authors
-------

- *Chathuranga Abeyrathna* - [github](https://github.com/chaturanga50/)

Contributors
------------

- *Iruka Rupasinghe* - [github](https://github.com/Rupasinghe2012/)

License
-------

opsworks-cli is licensed under the [Apache 2.0 License](LICENSE)
