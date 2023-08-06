# ndx-spectrum Extension for NWB:N

[Python Installation](#python-installation)

[Python Usage](#python-usage)
    
### Python Installation
```bash
pip install git+https://github.com/bendichter/ndx-spectrum.git
```

### Python Usage

```python
from ndx_spectrum import Spectrum
from datetime import datetime
from pynwb import NWBFile

nwb = NWBFile('session_description', 'identifier', datetime.now().astimezone())

spectrum = Spectrum('test_spectrum', frequencies=[1.,2.,3.], power=[1.,2.,3.],
                    phase=[1.,2.,3.])
```