from argparse import ArgumentParser
from . import generate

def parser():
    parser = ArgumentParser(description="Generate files from a template")
    parser.add_argument('template',
        help="The definition of the template")
    parser.add_argument('--target', '-d', default='.',
        help="Render the template into this target directory (default: cwd)")
    return parser

def main():
    p = parser()
    args = p.parse_args()
    with open(args.template) as f:
        defn = f.read()
    cwd = args.target
    generate.build_files(defn, cwd)
