<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/env-strip.svg?longCache=True)](https://pypi.org/project/env-strip/)

#### Installation
```bash
$ [sudo] pip install env-strip
```

#### Executable modules
usage|`__doc__`
-|-
`python -m env_strip path` |strip comments and blank lines from env file

#### Examples
`.env`
```bash
SECRET_KEY="https://www.youtube.com/channel/UCTZUTvv_1Onm-f-533Hyurw"

# postgres settings:
DB_NAME="name"
DB_USER="postgres"
DB_HOST="127.0.0.1"
DB_PORT=5432
```

```bash
$ python -m env_strip .env
SECRET_KEY=https://www.youtube.com/channel/UCTZUTvv_1Onm-f-533Hyurw
DB_NAME=name
DB_USER=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>