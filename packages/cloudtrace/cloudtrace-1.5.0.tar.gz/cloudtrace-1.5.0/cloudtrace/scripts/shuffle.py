import os
import subprocess
import tempfile
from argparse import ArgumentParser
from shutil import copyfile


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-I', '--inplace', action='store_true')
    group.add_argument('-o', '--output')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-z', '--gzip')
    group.add_argument('-b', '--bzip2')
    args = parser.parse_args()

    f = None
    fname = None

    try:
        if args.input.endswith('.gz'):
            infile = 'zcat'
        elif args.input.endswith('.bz2'):
            infile = 'bzcat'
        else:
            infile = 'cat'
        infile += ' {}'.format(args.input)
        if args.inplace:
            f, fname = tempfile.mkstemp()
            outfile = fname
        else:
            outfile = args.output
        if args.gzip or outfile.endswith('.gz') or (args.inplace and args.input.endswith('.gz')):
            out = '| gzip >'
        elif args.bzip2 or outfile.endswith('.bz2') or (args.inplace and args.input.endswith('.bz2')):
            out = '| bzip2 >'
        else:
            out = '>'
        out = '{} {}'.format(out, outfile)
        cmd = '{} | shuf {}'.format(infile, out)
        print(cmd)
        subprocess.run(cmd, shell=True)
        if args.inplace:
            copyfile(fname, args.input)
            # subprocess.run('cp {} {}'.format(fname, args.input))
            # f.close()
    finally:
        if f is not None and fname is not None:
            os.unlink(fname)


if __name__ == '__main__':
    main()
