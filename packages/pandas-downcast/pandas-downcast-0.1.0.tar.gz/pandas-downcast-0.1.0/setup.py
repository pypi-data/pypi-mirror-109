# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdcast']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.24']

extras_require = \
{':python_version < "3.7"': ['numpy>=1.16.5', 'dataclasses'],
 ':python_version >= "3.7"': ['numpy>=1.17']}

setup_kwargs = {
    'name': 'pandas-downcast',
    'version': '0.1.0',
    'description': 'Automated downcasting for Pandas DataFrames.',
    'long_description': 'Pandas Downcast\n===============\n\n[![image](https://img.shields.io/pypi/v/pandas-downcast.svg)](https://pypi.python.org/pypi/pandas-downcast)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pandas-downcast.svg)](https://pypi.python.org/pypi/pandas-downcast/)\n[![Build Status](https://travis-ci.com/domvwt/pandas-downcast.svg?branch=main)](https://travis-ci.com/domvwt/pandas-downcast)\n[![codecov](https://codecov.io/gh/domvwt/pandas-downcast/branch/main/graph/badge.svg?token=TQPLURKQ9Z)](https://codecov.io/gh/domvwt/pandas-downcast)\n\nSafely infer minimum viable schema for Pandas `DataFrame` and `Series`.\n\n## Installation\n```bash\npip install pandas-downcast\n```\n\n## Dependencies\n* python >= 3.6\n* pandas\n* numpy\n\n## License\n[MIT](https://opensource.org/licenses/MIT)\n\n## Usage\n```python\nimport pdcast as pdc\n\nimport numpy as np\nimport pandas as pd\n\ndata = {\n    "integers": np.linspace(1, 100, 100),\n    "floats": np.linspace(1, 1000, 100).round(2),\n    "booleans": np.random.choice([1, 0], 100),\n    "categories": np.random.choice(["foo", "bar", "baz"], 100),\n}\n\ndf = pd.DataFrame(data)\n\n# Downcast DataFrame to minimum viable schema.\ndf_downcast = pdc.downcast(df)\n\n# Infer minimum schema from DataFrame.\nschema = pdc.infer_schema(df)\n\n# Coerce DataFrame to schema - required if converting float to Pandas Integer.\ndf_new = pdc.coerce_df(df)\n```\n\n## Additional Notes\nSmaller types == smaller memory footprint.\n```python\ndf.info()\n# <class \'pandas.core.frame.DataFrame\'>\n# RangeIndex: 100 entries, 0 to 99\n# Data columns (total 4 columns):\n#  #   Column      Non-Null Count  Dtype  \n# ---  ------      --------------  -----  \n#  0   integers    100 non-null    float64\n#  1   floats      100 non-null    float64\n#  2   booleans    100 non-null    int64  \n#  3   categories  100 non-null    object \n# dtypes: float64(2), int64(1), object(1)\n# memory usage: 3.2+ KB\n\ndf_downcast.info()\n# <class \'pandas.core.frame.DataFrame\'>\n# RangeIndex: 100 entries, 0 to 99\n# Data columns (total 4 columns):\n#  #   Column      Non-Null Count  Dtype   \n# ---  ------      --------------  -----   \n#  0   integers    100 non-null    uint8   \n#  1   floats      100 non-null    float32 \n#  2   booleans    100 non-null    bool    \n#  3   categories  100 non-null    category\n# dtypes: bool(1), category(1), float32(1), uint8(1)\n# memory usage: 932.0 bytes\n```\n\nNumerical data types will be downcast if the resulting values are within tolerance of the original values.\nFor details on tolerance for numeric comparison, see the notes on [`np.allclose`](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html).\n```python\nprint(df.head())\n#    integers  floats  booleans categories\n# 0       1.0    1.00         1        foo\n# 1       2.0   11.09         0        baz\n# 2       3.0   21.18         1        bar\n# 3       4.0   31.27         0        bar\n# 4       5.0   41.36         0        foo\n\nprint(df_downcast.head())\n#    integers     floats  booleans categories\n# 0         1   1.000000      True        foo\n# 1         2  11.090000     False        baz\n# 2         3  21.180000      True        bar\n# 3         4  31.270000     False        bar\n# 4         5  41.360001     False        foo\n\n\nprint(pdc.options.ATOL)\n# >>> 1e-08\n\nprint(pdc.options.RTOL)\n# >>> 1e-05\n```\nTolerance can be set at module level or passed in function arguments:\n```python\npdc.options.ATOL = 1e-10\npdc.options.RTOL = 1e-10\ndf_downcast_new = pdc.downcast(df)\n```\nOr\n```python\ninfer_dtype_kws = {\n    "ATOL": 1e-10,\n    "RTOL": 1e-10\n}\ndf_downcast_new = pdc.downcast(df, infer_dtype_kws=infer_dtype_kws)\n```\nThe `floats` column is now kept as `float64` to meet the tolerance requirement. \nValues in the `integers` column are still safely cast to `uint8`.\n```python\ndf_downcast_new.info()\n# <class \'pandas.core.frame.DataFrame\'>\n# RangeIndex: 100 entries, 0 to 99\n# Data columns (total 4 columns):\n#  #   Column      Non-Null Count  Dtype   \n# ---  ------      --------------  -----   \n#  0   integers    100 non-null    uint8   \n#  1   floats      100 non-null    float64 \n#  2   booleans    100 non-null    bool    \n#  3   categories  100 non-null    category\n# dtypes: bool(1), category(1), float64(1), uint8(1)\n# memory usage: 1.3 KB\n```\n\n',
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/domvwt/pandas-downcast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
