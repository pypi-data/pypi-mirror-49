import pytest
from IPython.display import HTML
import pandas as pd
import numpy as np

from pandastabletooltip import main


def test_make_table_html_with_tooltip():
    df = pd.DataFrame(data=[{
        'a': 100,
        'b': 200,
        'c': 300,
    }, {
        'a': 1000,
        'b': 2000,
        'c': 3000,
    }])
    html = main.make_table_html_with_tooltip(df=df)
    assert isinstance(html, HTML)
    expected_html_str = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-aligh: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td title="0, a">100</td>
      <td title="0, b">200</td>
      <td title="0, c">300</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <th>1</th>
      <td title="1, a">1000</td>
      <td title="1, b">2000</td>
      <td title="1, c">3000</td>
    </tr>
  </tbody>
</table>"""
    assert html.data == expected_html_str

    df = pd.DataFrame(columns=['a'], index=np.arange(0, 3001))
    with pytest.raises(ValueError):
        main.make_table_html_with_tooltip(df)
