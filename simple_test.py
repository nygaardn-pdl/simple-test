from pathlib import Path

import pandas as pd
import requests


# replace 'x-api-key' value with your PDL API Key
# get your key here: https://dashboard.peopledatalabs.com/main/api-keys
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'x-api-key': 'YOUR API KEY HERE'
}


def enrich_company(name: str, website: str, linkedin: str) -> dict:
    '''
    Call the PDL Company Enrichment API for the given company.

    Company Enrichment API Documentation:
        https://docs.peopledatalabs.com/docs/company-enrichment-api

    Parameters
    ----------
    name : str
      Company name (ex: 'google')
    website : str
      Company website (ex: 'google.com')
    linkedin : str
      Company LinkedIn page URL (ex: 'linkedin.com/company/google')

    Returns
    -------
    Enrichment API JSON response as dict

    Raises
    -------
    ValueError : Raised if response does not have 200 Success status code
    '''
    resp = requests.get(
        'https://api.peopledatalabs.com/v5/company/enrich',
        headers=headers,
        params={
            'name':    name,
            'website': website,
            'profile': linkedin
        }
    )
    if resp.status_code != 200:
        raise ValueError(f'Request to {resp.request.url} failed. '
                         f'Response: {resp.status_code} - {resp.text}')

    return resp.json()


def filter_for_tag(to_filter: pd.DataFrame, tags: [str]) -> pd.DataFrame:
    '''
    Filter DataFrame to only the rows that contain a tag in the list

    Parameters
    ----------
    to_filter : DataFrame
      The DataFrame to filter
    tags : list of strings
      Keep any row that has at least one tag in this list

    Returns
    -------
    Filtered DataFrame
    '''
    # create a mask (True/False) for if each row has any of the tags
    mask = to_filter['tags'].dropna().apply(
        lambda row: any([tag in row for tag in tags]))

    # apply mask to filter DataFrame
    return to_filter[mask]


if __name__ == '__main__':
    # folder where the starting list is saved & where final CSVs will save to
    csv_location = Path(__file__).parent.resolve()
    initial_list = csv_location / 'starting_list.csv'

    # Load company dataset into pandas DataFrame
    print(f'Loading file: {initial_list}')
    initial_df = pd.read_csv(initial_list, header=0)
    print(f'Data Size: {initial_df.shape}')
    print(f'Data Columns: {initial_df.columns.tolist()}')

    # enrich each company using PDL's Company Enrichment API
    print('Enriching companies...')
    enriched_df = initial_df.apply(
        lambda row: enrich_company(
            row['name'],
            row['website'],
            row['linkedin_url']
        ),
        result_type='expand',
        axis=1
    )
    print(enriched_df.head())
    print(f'Enriched Data Columns: {enriched_df.columns.tolist()}')

    # if you want to save the intermediate results so that
    # you don't have to spend PDL credits every time, you
    # can export each DataFrame as a CSV and load it the
    # next time you run the script instead of making the request
    enriched_df.to_csv(csv_location / 'enriched_companies.csv')
    # enriched_df = pd.read_csv(
    #     csv_location / 'enriched_companies.csv', header=0)

    # find all companies with the tag 'saas'
    print('Filtering for tag = "saas"...')
    saas_df = filter_for_tag(enriched_df, ['saas'])
    print(saas_df.head())
    print(f'Found {len(saas_df.index)} companies with "saas" tag')

    print(
        f'Exporting list to: {(csv_location / "saas_companies.csv").resolve()}')
    saas_df.to_csv(csv_location / 'saas_companies.csv')
