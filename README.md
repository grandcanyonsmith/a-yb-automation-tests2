
# Yearbook Testing

This Python script is used to automate the testing of the Yearbook product. It uses the Playwright library to automate browser actions and pytest for testing. The script also integrates with TestRail, a test case management tool, to upload test results.

## Prerequisites

- Python 3.11
- Playwright
- pytest
- requests
- logger

You can install the necessary libraries with pip:

```bash
pip3 install -r requirements.txt
```

After installing the Playwright library, you need to run the following command to download the necessary browser binaries:

```bash
playwright install
```

## Environment Variables

This are set inside tests/helpers/{folder}/config.ini
[testrail]
run_id = 
case_id = 
url = 
email = 
password =

## Running the Tests

You can run the tests with pytest. For example, to run the celebrations tests, run the following command:

```bash
pytest celebrations_tests.py
```
or for legacy
```bash
pytest tests/legacy/ui_tests/
```


The test results will be uploaded to TestRail.



## Python Style Guide
1. Docstrings
- Use docstrings to describe what a function does.
- Should be between 3-8 words per line.
- If possible use triple quotes for docstrings and keep them on a single line.

2. Constants/Variables
- Should always be in all caps.
- Should be declared at the top of the file.

