"""The clean_file module and script."""

from __future__ import absolute_import

__author__ = 'Thomas Harrison'
__email__ = 'twh2898@vt.edu'
__license__ = 'MIT'
__version__ = '0.1.0'

import logging
from progress.bar import IncrementalBar
import lvx
from lvx.lvx import LvxFileReader, LvxFileWriter, LvxHeader


if __name__ == '__main__':
    msg_fmt = '%(message)s'
    logging.basicConfig(format=msg_fmt)


log = logging.getLogger(__name__)


def _log_header(h: LvxHeader, prefix: str = "header"):
    log.debug('%s.signature = %s', prefix, h.signature)
    log.debug('%s.version = %s', prefix, h.version)
    log.debug('%s.magic_code = %s', prefix, h.magic_code)
    log.debug('%s.frame_duration = %d ms', prefix, h.frame_duration)
    log.debug('%s.device_count = %d', prefix, h.device_count)
    for i, device in enumerate(h.devices):
        log.debug('%s.device[%d].lidar_broadcast_code = %s',
                  prefix, i, device.lidar_broadcast_code)
        log.debug('%s.device[%d].hub_broadcast_code = %s',
                  prefix, i, device.hub_broadcast_code)
        log.debug('%s.device[%d].device_index = %s',
                  prefix, i, device.device_index)
        log.debug('%s.device[%d].device_type = %s',
                  prefix, i, device.device_type)
        log.debug('%s.device[%d].extrinsic_enabled = %d',
                  prefix, i, device.extrinsic_enabled)
        log.debug('%s.device[%d].roll = %f', prefix, i, device.roll)
        log.debug('%s.device[%d].pitch = %f', prefix, i, device.pitch)
        log.debug('%s.device[%d].yaw = %f', prefix, i, device.yaw)
        log.debug('%s.device[%d].x = %f', prefix, i, device.x)
        log.debug('%s.device[%d].y = %f', prefix, i, device.y)
        log.debug('%s.device[%d].z = %f', prefix, i, device.z)


def clean_file(file: str, out_file: str):
    """Remove all but the first device and write to a new file."""
    log.info('clean_file %s to %s', file, out_file)

    with open(file, 'rb') as fi, open(out_file, 'wb') as fo:
        lvx_in = LvxFileReader(fi)

        # Print the header from the input file
        h = lvx_in.header
        _log_header(h, 'in_header')

        # Remove all duplicate devices
        device_dict = {d.lidar_broadcast_code: d for d in h.devices}
        h.devices = list(device_dict.values())
        h.device_count = len(h.devices)
        # Print the new output header
        _log_header(h, 'out_header')

        lvx_out = LvxFileWriter(h, fo)

        bar = None
        if __name__ == '__main__':
            bar = IncrementalBar('Processing', max=lvx_in.end,
                                 suffix='%(percent)d%% [%(elapsed_td)s / %(eta_td)s]')

        try:
            for frame in lvx_in:
                if bar:
                    bar.goto(frame._in_pos)

                lvx_out.write_frame(frame, fix_offset=True)
        finally:
            if bar:
                bar.finish()

        log.info('Done')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('clean_file',
                                     description='Attempt to fix a mis-formatted .lvx file')
    parser.add_argument('file',
                        help='the input file')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {} (lvx {})'.format(__version__, lvx.__version__))
    parser.add_argument('-v', '--verbose',
                        help='verbose output',
                        action='store_true')
    parser.add_argument('-o',
                        help='the output file (default: output.lvx)',
                        default='output.lvx',
                        dest='output')

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try:
        clean_file(args.file, out_file=args.output)
    except KeyboardInterrupt:
        print('Exiting!')
