# AnimatedGraphs

Build and awesome animated graph easily
![](https://github.com/lgbaeza/py-animated-graph/raw/master/news_sample.gif)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install AnimatedGraphs.

```bash
pip install AnimatedGraphs
```

## Usage

```python
import AnimatedGraphs as ag
from AnimatedGraphs import AnimatedBar as agBar

GRAPH_FILENAME = agBar.CreateGraphBar(
    dataset,
    args**
)
if (GRAPH_FILENAME != ""):
    print("Succeed. Animated grahBar available at {}" + GRAPH_FILENAME)
else:
    print("something went wrong")
```

You can find a notebook with sample usage here ![](https://github.com/lgbaeza/py-animated-graph)

## Args** details

| Argument                      | Required?     | Possible Values        | Default value / action |
| -------------                 | ------------- | --------------         | -------------          |
| DS                            |  Yes          |  numpy arr             |                        |
| AGGREGATION_TYPE              |  Yes          |  "COUNT", "SUM"        |                        |
| AGGREGATION_ATTRIBUTE_NAME    |  when AGG=SUM |  String                |                        |
| BAR_ATTRIBUTE_NAME            |  Yes          |  String                |                        |
| LOOP_ATTRIBUTE_NAME           |  Yes          |  String                |                        |
| SERIES_ATTRIBUTE_NAME         |  Yes          |  String                |                        |
| SERIES_ATTRIBUTE_NAME         |  Yes          |  String                |                        |
| GRAPH_XLABEL                  |  Opcional     |  String                | Empty                  |
| GRAPH_XLABEL                  |  Opcional     |  String                | Empty                  |
| IMAGE_SET_URL                 |  Opcional     |  String: URL to Zip    | <No image>             |
| IMAGE_SET_EXT                 |  Opcional     |  String                | <No image>             |
| SORT_BARS_LIST                |  Opcional     |  Array of String       | <No sorting>           |
| GRAPH_STEPS                   |  Opcional     |  Integer               | 10                     |
| GRAPH_FRAME_DURATION          |  Opcional     |  Float (0-3]           | 1.0                    |
| GRAPH_FILENAME                |  Opcional     |  String                | "animated-graph.gif"   |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)