def add_country_codes(data: pd.DataFrame) -> pd.DataFrame:
    country_codes = pd.read_csv('data/iso_country_codes.csv')[['Alpha-3 code', 'English short name lower case']].rename(columns = {
        'Alpha-3 code': 'iso3',
        'English short name lower case': 'country'
    })
    data = data.merge(country_codes)
    return data