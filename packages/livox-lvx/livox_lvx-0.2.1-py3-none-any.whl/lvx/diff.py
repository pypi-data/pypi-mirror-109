"""The diff module and script."""

from __future__ import absolute_import

__author__ = 'Thomas Harrison'
__email__ = 'twh2898@vt.edu'
__license__ = 'MIT'
__version__ = '0.1.0'

import logging
from progress.bar import IncrementalBar
import lvx
from lvx.lvx import LvxFileReader, LvxHeader


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


def diff(file: str, out_file: str, header_only: bool = False):
    """Write a human readable representation of a .lvx file for use with the diff tool."""
    log.info('diff %s to %s', file, out_file)

    with open(file, 'rb') as fi, open(out_file, 'w') as fo:
        lvx_in = LvxFileReader(fi)

        # Print the header from the input file
        h = lvx_in.header
        _log_header(h, 'in_header')

        bar = None
        if __name__ == '__main__' and not header_only:
            bar = IncrementalBar('Processing', max=lvx_in.end,
                                 suffix='%(percent)d%% [%(elapsed_td)s / %(eta_td)s]')
            bar.start()

        print('file =', file, file=fo)
        print('public.signature =', h.signature, file=fo)
        print('public.version =', h.version, file=fo)
        print('public.magic_code =', h.magic_code, file=fo)
        print('private.frame_duration =', h.frame_duration, file=fo)
        print('private.device_count =', h.device_count, file=fo)
        for i, dev in enumerate(h.devices):
            print('deviceInfo[{}].lidar_broadcast_code ='.format(
                i), dev.lidar_broadcast_code, file=fo)
            print('deviceInfo[{}].hub_broadcast_code ='.format(
                i), dev.hub_broadcast_code, file=fo)
            print('deviceInfo[{}].device_index ='.format(
                i), dev.device_index, file=fo)
            print('deviceInfo[{}].device_type ='.format(
                i), dev.device_type, file=fo)
            print('deviceInfo[{}].extrinsic_enabled ='.format(
                i), dev.extrinsic_enabled, file=fo)
            print('deviceInfo[{}].roll ='.format(i), dev.roll, file=fo)
            print('deviceInfo[{}].pitch ='.format(i), dev.pitch, file=fo)
            print('deviceInfo[{}].yaw ='.format(i), dev.yaw, file=fo)
            print('deviceInfo[{}].x ='.format(i), dev.x, file=fo)
            print('deviceInfo[{}].y ='.format(i), dev.y, file=fo)
            print('deviceInfo[{}].z ='.format(i), dev.z, file=fo)

        if not header_only:
            try:
                for i, frame in enumerate(lvx_in):
                    if bar:
                        bar.goto(frame._in_pos)

                    print('# Actual position', frame._in_pos, file=fo)
                    print('frame[{}].header.current_offset ='.format(
                        i), frame.header.current_offset, file=fo)
                    print('frame[{}].header.next_offset ='.format(
                        i), frame.header.next_offset, file=fo)
                    print('frame[{}].header.frame_index ='.format(
                        i), frame.header.frame_index, file=fo)
            finally:
                if bar:
                    bar.finish()

        log.info('Done')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('diff',
                                     description='Produce a pain text representation of a .lvx file for use with the diff tool')
    parser.add_argument('file',
                        help='the input file')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {} (lvx {})'.format(__version__, lvx.__version__))
    parser.add_argument('-v', '--verbose',
                        help='verbose output',
                        action='store_true')
    parser.add_argument('-o',
                        help='the output file (default: output.diff)',
                        default='output.diff',
                        dest='output')
    parser.add_argument('--header-only',
                        help='skip writing the frames',
                        action='store_true')

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try:
        diff(args.file, out_file=args.output, header_only=args.header_only)
    except KeyboardInterrupt:
        print('Exiting!')
