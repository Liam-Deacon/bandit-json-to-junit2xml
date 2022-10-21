# bandit-json-to-junit2xml

Provides a script for crudely converting bandit JSON output to JUnit2 compatible XML

## Installation

> **Note**: There is not currently any package, so simply download and use directly. 

```shell
curl https://raw.githubusercontent.com/Liam-Deacon/bandit-json-to-junit2xml/main/bandit_json_to_junit2xml.py > bandit_json_to_junit2xml.py
chmod +x bandit_json_to_junit2xml.py  # optional step
```

## Usage

To convert from `bandit` JSON to JUnit2 XML, then simply do:

```shell
bandit ${BANDIT_FLAGS} --format=json . | python3 bandit_json_to_junit2xml.py > bandit-report.xml
```

## TODO

- [ ] - Create package and entrypoint script
- [ ] - Publish to PyPI
- [ ] - Handle command line arguments rather than just plain pipe via `stdin`
