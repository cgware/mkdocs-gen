import argparse
import os
import shutil
from pathlib import Path

OUTPUT_DIR = 'mkdocs'
TMPL_DIR = "tmpl"

CSS = """.wy-nav-top {
    background-color: #131313 !important;
    box-shadow: 0 0 .2rem rgba(0, 0, 0, .1), 0 .2rem .4rem rgba(0, 0, 0, .2);
    align-items: center !important;
    padding: 0;
}

.wy-nav-top .fa {
    color: #9ca0a5 !important;
    font-size: 24px !important;
    padding: 12px !important;
}

.wy-nav-side {
    padding: 0 !important;
}

.wy-nav-content {
    background-color: #131313 !important;
    max-width: none !important;
}

.wy-nav-content-wrap {
    background-color: #131313 !important;
}

body {
    color: #D0D0D0 !important;
}

.wy-side-nav-search {
    background-color: #1A1A1A !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    padding-bottom: 0 !important;
}

input {
    color: #D0D0D0 !important;
    background-color: #1A1A1A !important;
    border-color: #333333 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

.wy-side-scroll {
    background-color: #1A1A1A !important;
    padding: 0 !important;
}

.caption-text {
    color: #868686 !important;
}

.wy-menu-vertical li.current a {
    background-color: #1A1A1A !important;
    border: 0 !important;
}

code {
    background-color: #202020 !important;
    color: #D2D2D2 !important;
    border-color: #333333 !important;
    border-radius: .2em !important;
}

.hljs {
    background-color: #1A1A1A !important;
}

::-webkit-scrollbar {
    width: 10px !important;
    height: 6px !important;
}

::-webkit-scrollbar-thumb {
    background: #666666 !important;
}

::-webkit-scrollbar-track {
    background: #1A1A1A !important;
}

.btn {
    background-color: #131313 !important;
    color: #FF8C42 !important;
    border-color: #333333 !important;
    border-radius: .2em !important;
    box-shadow: none !important;
}

.btn:visited {
    color: #FF8C42 !important;
}

a {
    color: #FF8C42 !important;
    text-decoration: none !important;
}

hr {
    background-color: #333333;
    border: 0;
}

footer {
    display: none;
}
"""

YML = """site_name: {name}
theme: readthedocs
extra_css:
  - css/extra.css
nav:
  - Home: README.md
"""


def error(msg: str):
	print(msg)
	exit(1)


def gen_css(out: Path):
	out = out / 'docs' / 'css'

	if not out.exists():
		os.makedirs(out)

	out /= 'extra.css'

	with open(out, 'w') as file:
		file.write(CSS)


def gen_yml(out: Path, name: str):
	if not out.exists():
		os.makedirs(out)

	out /= 'mkdocs.yml'

	yml = YML.replace('{name}', name)

	with open(out, 'w') as file:
		file.write(yml)


def copy_file(src: Path, dest: Path):

	if not src.exists():
		error(f'ERROR: File not found: {src}')

	if dest.exists():
		os.remove(dest)

	try:
		shutil.copy(src, dest)
	except Exception as e:
		error(f'ERROR: Failed to copy: {e}')


def main(args):
	out = Path(OUTPUT_DIR)
	gen_css(out)
	gen_yml(out, args.name)
	copy_file(Path('README.md'), out / 'docs' / 'README.md')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate mkdocs')
	parser.add_argument('-n', '--name', type=str, help='package name', required=True)

	main(parser.parse_args())
