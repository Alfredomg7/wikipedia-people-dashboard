import polars as pl

def format_metric(metric):
    if metric == 'total_views_sum' or 'views_sum':
        return 'Total Views'
    else:
        return metric.capitalize()
    
def get_top_entries(df, location_type, location, n=20):
    location_df = df.filter(pl.col(location_type) == location)

    grouped_df = (
        location_df
        .group_by('name')
        .agg(pl.col('views_sum').sum())
    )

    top_entries_df = (
        grouped_df
        .sort('views_sum')
        .tail(n)
    )

    return top_entries_df
