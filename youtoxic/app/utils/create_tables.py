"""Defines functions used for creating tables.

"""
import dash_table


def create_tweets_table(df, table_columns):
    """Creates a DataTable from tweet data.

    Parameters
    ----------
    df : DataFrame
        A DataFrame containing information about tweets.
    table_columns : list of str
        A list containing the information needed to create a DataTable from the given DataFrame.

    Returns
    -------
    DataTable
        The DataTable containing the given information.

    """
    table = dash_table.DataTable(
        id="table",
        columns=table_columns,
        data=df.to_dict("rows"),
        style_table={"border": "thin black solid"},
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "rgb(150,150,150)",
            "textAlign": "center",
        },
        style_cell={
            "textAlign": "left",
            "fontFamily": "optima",
            "border": "thin lightgrey solid",
            "padding": 15,
        },
        style_data={"whiteSpace": "normal"},
        css=[
            {
                "selector": ".dash-cell div.dash-cell-value",
                "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
            }
        ],
        merge_duplicate_headers=True,
        sorting=True,
        pagination_mode="fe",
        pagination_settings={"displayed_pages": 1, "current_page": 0, "page_size": 25},
    )

    return table
