# simple-test
This script is a simple test for using PDL APIs and poetry.

The script will:
1. Read a [CSV of companies](./starting_list.csv)
2. Run the PDL [Company Enrichment API](https://docs.peopledatalabs.com/docs/company-enrichment-api) for each
3. Filter for companies with a specific tag
4. Export the filtered list as a CSV

## To Run
1. Set `'x-api-key'` in headers object
2. Run using poetry:
    ```shell
    % cd simple-test/
    % poetry init
    % poetry run python simple_test.py
    ```
