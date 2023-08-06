# CerebralCortex-Random-Data-Generator
Generate some random data for Cerebral Cortex Demo Purposes. This script will generate one day worth of sensors data.

### Dependencies
* Python 3.5, 3.6, 3.7, 3.8
* cerebralcortex-kernel - 3.3.9
    * ```pip3 install cerebralcortex-kernel```

### How to run
* ``python3 main.py``
* By default, random generated data will be stored under home folder, e.g.,``(/Users/ali/cc_data/)``

### How to read generated data
* All the data is stored in parquet files format
* Use CerebralCortex to read the data/metadata
```$xslt
from cerebralcortex.kernel import Kernel

CC = Kernel(cc_configs="default", study_name="mguard")
data = CC.get_stream("battery--org.md2k.phonesensor--phone")
data.show()
```

### Available stream names
* `org.md2k--mguard--00000000-e19c-3956-9db2-5459ccadd40c--battery--phone`
* `org.md2k--mguard--00000000-e19c-3956-9db2-5459ccadd40c--location--phone`
* `org.md2k--mguard--00000000-e19c-3956-9db2-5459ccadd40c--data_analysis--gps_episodes_and_semantic_location`
* `org.md2k--mguard--00000000-e19c-3956-9db2-5459ccadd40c--accelerometer--phone`
* `org.md2k--mguard--00000000-e19c-3956-9db2-5459ccadd40c--gyroscope--phone`

### Google Colab Notebook
https://colab.research.google.com/drive/1nxQom7FpzTLEblv_uBbtHUD8TaTN48I5?usp=sharing