## Usage
```python
import toh5py


to_h5py.do(image_list = ['../../1.png', '../../2.png', '../../3.png', ...],
           label_list = ['1', '2', '2', '3', ...],
           ratio = 0.8，
           data_shape = (0, 256, 256, 3)，
           rollaxis = False，
           output = 'output.hdf5')
```
