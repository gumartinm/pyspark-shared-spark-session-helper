[![Build Status](https://travis-ci.org/gumartinm/pyspark-shared-spark-session-helper.svg?branch=master)](https://travis-ci.org/gumartinm/pyspark-shared-spark-session-helper)

PySpark: unit, integration and end to end tests.
=========================


## Building

### Prerequisites

In order to build this project [**poetry**](https://python-poetry.org/docs/) and [**JVM 8**](https://adoptopenjdk.net/?variant=openjdk8&jvmVariant=hotspot) must be available in your environment.

### Command

```
poetry install
poetry run pylint --output-format=colorized --fail-under=8 src/ tests/
poetry run pycodestyle --config pycodestyle.ini src/ tests/
poetry run pytest
poetry build
```



