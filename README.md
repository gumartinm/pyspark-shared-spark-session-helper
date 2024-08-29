[![Build Status](https://github.com/gumartinm/pyspark-shared-spark-session-helper/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/gumartinm/pyspark-shared-spark-session-helper/actions/workflows/master.yml)

PySpark: unit, integration and end to end tests.
=========================


## Building

### Prerequisites

In order to build this project [**poetry**](https://python-poetry.org/docs/) and [**JVM 8**](https://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot) must be available in your environment.

### Command

```
poetry install
poetry run ruff check
poetry run pylint --output-format=colorized --fail-under=8 src/ tests/
poetry run pycodestyle --config pycodestyle.ini src/ tests/
poetry run pytest
poetry build
```



