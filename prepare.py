import pandas as pd

def prepare_data(raw_data_path: str) -> pd.DataFrame:
    df = pd.read_csv(raw_data_path)

    df = df.drop(columns=['name', 'views_median', 'neighborhood', 'place'])

    valid_states = {
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", 
        "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", 
        "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
        "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", 
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
        "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
        "West Virginia", "Wisconsin", "Wyoming"
    }

    county_to_state = {
        "Brown County": "Wisconsin", "Calumet County": "Wisconsin", "Chemung County": "New York", 
        "Crawford County": "Wisconsin", "Dane County": "Wisconsin", "Dodge County": "Wisconsin", 
        "Fond du Lac County": "Wisconsin", "Franklin County": "New York", "Fulton County": "Georgia", 
        "Green County": "Wisconsin", "Herkimer County": "New York", "Iowa County": "Wisconsin", 
        "Jefferson County": "Wisconsin", "Kenosha County": "Wisconsin", "Kewaunee County": "Wisconsin", 
        "La Crosse County": "Wisconsin", "Lake County": "Illinois", "Los Angeles": "California", 
        "Manitowoc County": "Wisconsin", "Marquette County": "Wisconsin", "Milwaukee County": "Wisconsin", 
        "Monroe County": "New York", "Montgomery County": "New York", "Nassau County": "New York", 
        "Oneida County": "New York", "Orange County": "California", "Orleans County": "New York", 
        "Oswego County": "New York", "Outagamie County": "Wisconsin", "Racine County": "Wisconsin", 
        "Rancho Cucamonga": "California", "Rock County": "Wisconsin", "San Diego": "California", 
        "Saratoga County": "New York", "Sauk County": "Wisconsin", "Schoharie County": "New York", 
        "Sheboygan County": "Wisconsin", "Walworth County": "Wisconsin", "Washington County": "Wisconsin", 
        "Waukesha County": "Wisconsin", "Waupaca County": "Wisconsin", "Winnebago County": "Wisconsin", 
        "Yates County": "New York"
    }

    df['state'] = df['state'].apply(
        lambda x: x if x in valid_states else county_to_state.get(x, x)
    )

    columns_to_rename = {'name_clean': 'name'}
    df = df.rename(columns=columns_to_rename)

    return df 

def prepare_grouped_data(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
    grouped_df = (
        df.groupby(["name", group_by], as_index=False)
        .agg(
            total_views_sum=("views_sum", "sum"),
            lat=("lat", "median"),
            lng=("lng", "median"),
        )
    )

    max_views_idx = grouped_df.groupby(group_by)["total_views_sum"].idxmax()
    max_views_df = grouped_df.loc[max_views_idx].reset_index(drop=True)

    return max_views_df


def prepare():
    raw_data_path = "https://raw.githubusercontent.com/the-pudding/data/master/people-map/people-map.csv"
    prepared_data_path = "data/all_data.csv"
    city_data_path = "data/city-data.csv"
    state_data_path = "data/state-data.csv"

    prepared_df = prepare_data(raw_data_path)
    city_df = prepare_grouped_data(prepared_df, "city")
    state_df = prepare_grouped_data(prepared_df, "state")

    prepared_df.to_csv(prepared_data_path, index=False)
    city_df.to_csv(city_data_path, index=False)
    state_df.to_csv(state_data_path, index=False)

if __name__ == "__main__":
    prepare()