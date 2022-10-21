#! /usr/bin/env python3
"""Simple file for converting between bandit's JSON report output and JUnit2 compatible XML

Examples
--------

```shell
bandit --format json . | python bandit_json_to_junit2xml.py
```

"""

import json
import sys

import lxml.builder
import lxml.etree

#: Convenience variable as alternative to using lxml.etree.Element
elm = lxml.builder.ElementMaker()


def testsuites(*args, tests: int = 0, errors: int = 0, **kwargs) -> lxml.etree.Element:
    """Create a new <testsuites> element."""
    return elm.testsuites(tests=str(tests), errors=str(errors), *args, **kwargs)


def testsuite(
    *args,
    name: str = None,
    tests: int = 0,
    errors: int = 0,
    failures: int = 0,
    skipped: int = 0,
    time: int = 0,
    **kwargs,
) -> lxml.etree.Element:
    """Create a new <testsuite> element."""
    if not name:
        raise TypeError("name must be specified by keyword-argument")
    return elm.testsuite(
        name=name,
        tests=str(tests),
        errors=str(errors),
        failures=str(failures),
        skipped=str(skipped),
        time=str(time),
        *args,
        **kwargs,
    )


def testcase(
    *args, name: str = None, filename: str = None, classname: str = None, line: int = None, **kwargs
) -> lxml.etree.Element:
    """Create a new <testcase> XML element."""
    if not name:
        raise ValueError("name must be specified by keyword-argument")
    if not filename:
        raise ValueError("filename must be specified by keyword-argument")
    if line:
        kwargs["line"] = str(line)
    return elm.testcase(*args, name=name, classname=classname or filename, file=filename, **kwargs)


def failure(text: str, *args, message: str, type="ERROR", **kwargs) -> lxml.etree.Element:
    """Create a new <failure> XML element."""
    return elm.failure(text, *args, type=type, message=message, **kwargs)


def error(*args, **kwargs) -> lxml.etree.Element:
    """Create a new <error> XML element.""" 
    return elm.error(*args, **kwargs)


def parse_result(result: dict) -> lxml.etree.Element:
    """Transform `result` dictionary from loaded bandit JSON into a <testcase> element block."""
    data = failure(
        (
            f"{result['test_id']}: {result['test_name']} "
            f"[severity={result['issue_severity']}, confidence={result['issue_confidence']}]"
        ),
        type="ERROR",
        message=(
            f"{result['issue_text']}.\r\n"
            f"See {result['more_info']} and {result['issue_cwe']['link']} for more information."
        ),
    )
    return testcase(
        data,
        name=f"bandit.issue.{result['issue_text']}",
        filename=result["filename"].lstrip("./"),
        line=result["line_number"],
    )


def parse_error(error_data: dict) -> lxml.etree.Element:
    """Transform `error_data` dictionary from loaded bandit JSON into a <testcase> element block.""" 
    return testcase(
        error(type="bandit.error", message=error_data["reason"]),
        name="bandit.error",
        filename=error_data["filename"].lstrip("./"),
        line=None,
    )


def parse_bandit_json_from_stdin() -> lxml.etree.Element:
    """Read in JSON report data from stdin and create an XML element document block.""" 
    data = json.loads(sys.stdin.read())
    doc = testsuites(
        testsuite(
            *list(map(parse_result, data["results"])),
            *list(map(parse_error, data["errors"])),
            name="bandit",
            tests=len(data["results"]),
            errors=len(data["errors"]),
        )
    )
    return doc


if __name__ == "__main__":
    doc = parse_bandit_json_from_stdin()
    print(lxml.etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8"))
