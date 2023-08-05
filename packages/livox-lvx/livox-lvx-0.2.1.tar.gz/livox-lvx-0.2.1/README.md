# livox_lvx

Library for reading, processing and writing `.lvx` files.

## Usage

```py
from lvx import LvxFileReader, LvxFileWriter

INPUT = '370132276011LIDAR.lvx'

with open(INPUT, 'rb') as fi, open(INPUT + '.other', 'wb') as fo:
    lvx_in = LvxFileReader(fi)
    header = lvx_in.header
    lvx_out = LvxFileWriter(header, fo)

    for frame in lvx_in:
        lvx_out.write_frame(frame, True)
```

### lvx.clean_file

The `lvx.clean_file` will remove any duplicate devices in the header device
block and updates the frame offsets while writing.

```py
from lvx import clean_devices

clean_devices('input.lvx', 'output.lvx')
```

#### Script

```sh
python -m lvx.clean_devices -h  # Show script help
python -m lvx.clean_devices input.lvx -o output.lvx
```

### lvx.diff

The `lvx.diff` function will write a plain text file with information about the
structure of the input file.

```py
from lvx import diff

diff('input.lvx', 'output.diff', header_only=False)
```

#### Script

```sh
python -m lvx.diff -h  # Show script help
python -m lvx.diff input.lvx -o output.diff
```

## Install

```sh
git clone https://gitlab.com/twh2898/livox_lvx
cd livox_lvx
pip install .
```

### Development Install

Replace the pip command in the above code with the following (note the `-e`).

```sh
pip install -e .
```

## Building

```sh
git clone https://gitlab.com/twh2898/livox_lvx
cd livox_lvx
pip install build
python -m build
```

## License

livox_lvx uses the [MIT](LICENSE) License.
