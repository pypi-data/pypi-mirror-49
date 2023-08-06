"""A module that handles tooltip display.
"""

import pandas as pd
from IPython.display import HTML, display


def make_table_html_with_tooltip(df, limit=3000):
    """
    Make a table with tooltips.

    Parameters
    ----------
    df : DataFrame
        DataFrame to be displayed.
    limit : int, default 3000
        Display limit number.

    Raises
    ------
    ValueError
        If the number of DataFrame rows exceeds the display
        limit number.

    Returns
    -------
    html : HTML
        Result HTML object.
    """
    if len(df) > limit:
        err_msg = 'The number of DataFrame rows exceeds the dispaly limit '\
                  '(currently limited {limit_num}). '\
                  'Please adjust the `limit` argument.'.format(
                      limit_num=limit)
        raise ValueError(err_msg)

    html_str = '<table border="1" class="dataframe">'
    html_str += '\n  <thead>'
    html_str += '\n    <tr style="text-aligh: right;">'
    html_str += '\n      <th></th>'
    for column in df.columns:
        html_str += '\n      <th>{column}</th>'.format(column=column)
    html_str += '\n    </tr>'
    html_str += '\n  </thead>'

    for index_val, sr in df.iterrows():
        html_str += '\n  <tbody>'
        html_str += '\n    <tr>'
        html_str += '\n      <th>{index_val}</th>'.format(
            index_val=index_val)
        for column_val, value in sr.iteritems():
            tooltip = '{index_val}, {column_val}'.format(
                index_val=index_val,
                column_val=column_val)
            html_str += \
                '\n      <td title="{tooltip}">'\
                '{value}</td>'.format(
                    tooltip=tooltip,
                    value=value)
        html_str += '\n    </tr>'
        html_str += '\n  </tbody>'
    html_str += '\n</table>'
    return HTML(html_str)
