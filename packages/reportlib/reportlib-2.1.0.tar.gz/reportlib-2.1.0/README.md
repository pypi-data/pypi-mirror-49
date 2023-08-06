# reportlib
Generator HTML from pandas via Jinja2

##  Changelog for version 2.0.0

- Change usage of EnvironParser: replace parse() method by some get methods for different types

- Replace options from Generator constructor by context kwargs. Generator's context now is passed to its tables.

- Add render_kwargs to Styler to save render context, so in `Generator.add_table` and `Generator.add_grouped_table` you don't need to pass context as an argument

- Add class rp-table-striped with different color for odd/even tr

- rp-table-hover now can support jupyter dark theme

# Usage
## Project structure
```
root/ (or root/src/)
 |-+-templates/
 | |-styles.css
 |-report.py
 |-email_config.yml
 |-metadata.yml
 ...
```

## Basic usage
```bash
# Setup environ before running code
export REPORT_DATE='2019-06-30'
export EMAIL_CONFIG_PATH='email_config.yml'
export EMAIL_ENV='dev'
export HTML_OUTPUT_PATH='report_output.html'
```


```python
"""report.py"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from reportlib import Generator, EnvironParser

# Parse options from env
environ = EnvironParser()
report_date = environ.date('REPORT_DATE', default='yesterday')

# Prepare data
df = pd.DataFrame(np.random.randn(8, 4), index=['index'], columns=['a', 'b', 'c', 'd'])

# Initial generator
generator = Generator(
  title='Report Demo',
  report_date=report_date,
)

# Styling data
style = (df.style
  .add_class('bold highlight', subset=pd.IndexSlice[0:1, style.data.columns])  # Bold and Highlight some row by using class `highlight`
  .add_class('text-right', columns=style.data.columns)  # Align right columns
)

# Add tables
generator.add_table(style)

# Run generator
generator.run()
```


```yaml
# This is `dev` env
dev: 
  smtp:
    username: 'your.email@your.domain'
    pwd: 'yourpassword'
  from: 'From'  
  subject: 'Report Demo - {report_date:%d/%m/%Y}'  # Report Demo - 30/06/2019
  to: 
    - 'you@your.domain'
  cc:
    - 'your.boss@your.domain'
  bcc:
    - 'some.body@other.domain'
  files:
    - 'relative_path/some_attachtments.txt'
    - '/home/users/you/absolute_path/attactment.txt'
# ... Your other env
```