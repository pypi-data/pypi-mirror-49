# reportlib
Generator HTML from pandas via Jinja2

# Usage
## Project structure
```
root (or root/src)
 |-report.py
 |-email_config.yml
 |-metadata.yml
 ...
```

## Basic usage
```python
"""report.py"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from reportlib import Generator, EnvironParser

# Update environ when run in jupyter. Comment this code when run via pipeline
os.environ.update({
    'PYSPARK_PYTHON': '/opt/conda/bin/python',
    'PYSPARK_DRIVER_PYTHON': '/opt/conda/bin/python',
    'REPORT_DATE': '2019-06-30',
    'HTML_OUTPUT_PATH': 'report_output.html',  # Export output to file
    'EMAIL_CONFIG_PATH': 'email_config.yml',  # Send output to somebody via email
    'EMAIL_ENV': 'dev',  # Provided env in `email_config.yml`
})

# Parse options from env
options = EnvironParser().parse()
report_date = options.get('REPORT_DATE', datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=1))

# Prepare data
df = pd.DataFrame(np.random.randn(8, 4), index=['index'], columns=['a', 'b', 'c', 'd'])

# Initial generator
generator = Generator(options)

# Styling data
style = df.style
style.add_class('bold highlight', subset=pd.IndexSlice[0:1, style.data.columns])  # Bold and Highlight some row by using class `highlight`
style.add_class('text-right', columns=style.data.columns)  # Align right columns

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
  subject: 'Report Demo - {REPORT_DATE:%d/%m/%Y}'  # Report Demo - 30/06/2019
  to: 
    - 'you@your.domain'
  cc:
    - 'your.boss@your.domain'
  bcc:
    - 'some.body@other.domain'
  files:
    - 'relative_path/some_attachtments.txt'
    - '/home/users/you/absolute_path/'
# ... Your other env
```