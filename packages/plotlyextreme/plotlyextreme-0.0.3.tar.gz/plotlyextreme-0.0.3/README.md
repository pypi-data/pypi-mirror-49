## PlotlyExtreme

Set of wrapper functions to abstract repetitive tasks related to plotting with
the plotly library.


### Current Plots

#### Plot a Big Number

`plots.create_big_number`

![Big Number](/img/plot_big_number.png?raw=true)

#### Plot Four Dimensions using Buttons

`plots.plot_four_dimensions`

![Four Dimensions with Annotations](/img/plot_four_dimensions.png?raw=true)


### Example

```
import pandas as pd
from plotlyextreme import plots

df = pd.DataFrame({
                    'abc':[1,2,3,1,1,2,3,1],
                    'def':[4,5,6,4,6,4,6,4],
                    'ghi':['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'],
                    'jkl':['z', 'z', 'z', 'z', 'y', 'y', 'y', 'y'],
                    'annotation_one': ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
                    'annotation_two': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                  })

plots.create_big_number(title='abc', large_number=123, pacing=.7)

plots.plot_four_dimensions(df, x='abc', y='def', title='alphabet', segmentation_col='ghi', button_col='jkl',
                           buttons=['z', 'y'], default_visibility='z')
```
