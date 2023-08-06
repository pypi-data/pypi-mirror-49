[![PyPI version fury.io](https://badge.fury.io/py/pylandstats.svg)](https://pypi.python.org/pypi/pylandstats/)
[![Documentation Status](https://readthedocs.org/projects/pylandstats/badge/?version=latest)](https://pylandstats.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/martibosch/pylandstats.svg?branch=master)](https://travis-ci.org/martibosch/pylandstats)
[![Coverage Status](https://coveralls.io/repos/github/martibosch/pylandstats/badge.svg?branch=master)](https://coveralls.io/github/martibosch/pylandstats?branch=master)
[![GitHub license](https://img.shields.io/github/license/martibosch/pylandstats.svg)](https://github.com/martibosch/pylandstats/blob/master/LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/martibosch/pylandstats-notebooks/master?filepath=overview.ipynb)

# PyLandStats

Open-source Pythonic library to compute landscape metrics within the PyData stack (NumPy, pandas, matplotlib...)

## Features

Read GeoTiff files of land use/cover

```python
import pylandstats as pls

ls = pls.read_geotiff('data/vaud_g100_clc00_V18_5.tif')

ls.plot_landscape(legend=True)
```

![landscape-vaud](figures/landscape.png)

Compute pandas DataFrames of landscape metrics at the patch, class and landscape level

```python
patch_metrics_df = ls.compute_patch_metrics_df()
patch_metrics_df.head()
```

| patch_id | class_val | area | perimeter | perimeter_area_ratio | shape_index | fractal_dimension | euclidean_nearest_neighbor |
| -------: | --------: | ---: | --------: | -------------------: | ----------: | ----------------: | -------------------------: |
|        0 |         1 |  115 |     10600 |                92.17 |       2.409 |             1.130 |                   1431.782 |
|        1 |         1 |   13 |      2600 |               200.00 |       1.625 |             1.100 |                    223.607 |
|        2 |         1 |    2 |       600 |               300.00 |       1.000 |             1.012 |                    223.607 |
|        3 |         1 |   69 |      6000 |                86.96 |       1.765 |             1.088 |                    316.228 |
|        4 |         1 |   76 |      8800 |               115.79 |       2.444 |             1.137 |                    316.228 |

```python
class_metrics_df = ls.compute_class_metrics_df(metrics=['proportion_of_landscape', 'edge_density'])
class_metrics_df
```

| class_val | proportion_of_landscape | edge_density |
| --------: | ----------------------: | -----------: |
|         1 |                   7.702 |        4.459 |
|         2 |                  92.298 |        4.459 |

Also analyze the spatio-temporal evolution of the landscape:

```python
input_fnames = [
    'data/vaud_g100_clc00_V18_5.tif',
    'data/vaud_g100_clc06_V18_5a.tif',
    'data/vaud_g100_clc12_V18_5a.tif'
]

sta = pls.SpatioTemporalAnalysis(
    input_fnames, metrics=[
        'proportion_of_landscape',
        'edge_density',
        'fractal_dimension_am',
        'landscape_shape_index',
        'shannon_diversity_index'
    ], classes=[1], dates=[2000, 2006, 2012], 
)

fig, axes = sta.plot_metrics(
    class_val=1,
    metrics=['proportion_of_landscape', 'edge_density', 'fractal_dimension_am'],
    num_cols=3)
fig.suptitle('Class-level metrics (urban)')
```

![spatiotemporal-analysis](figures/spatiotemporal.png)

See the [documentation](https://pylandstats.readthedocs.io/en/latest/?badge=latest) and the [pylandstats-notebooks](https://github.com/martibosch/pylandstats-notebooks) repository for a more complete overview.

## Installation

To install use pip:

    $ pip install pylandstats


If you want to use the `BufferAnalysis` class, you will need [geopandas](https://github.com/geopandas/geopandas). The easiest way to install it is via [conda-forge](https://conda-forge.org/) as in:

    $ conda install -c conda-forge geopandas
    
and then install PyLandStats with the `geo` extras as in:

    $ pip install pylandstats[geo]
    


## Acknowledgments

* With the support of the École Polytechnique Fédérale de Lausanne (EPFL)
* The Corine Land Cover datasets used for the test datasets were produced with funding by the European Union
