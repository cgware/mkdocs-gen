import argparse
import os
import shutil
from pathlib import Path

OUTPUT_DIR = 'mkdocs'

YML = """site_name: {name}
theme:
  name: null
  custom_dir: 'theme'
nav:
"""


def error(msg: str):
	print(msg)
	exit(1)


def add_page(nav: dict, src: Path, docs_path: str, name: str):

	if not src.exists():
		return

	dest = Path(OUTPUT_DIR) / 'docs' / docs_path

	if dest.exists():
		os.remove(dest)

	try:
		shutil.copy(src, dest)
	except Exception as e:
		error(f'ERROR: Failed to copy: {e}')

	nav[name] = docs_path


def gen_yml(name: str, nav: dict):
	out = Path(OUTPUT_DIR)

	if not out.exists():
		os.makedirs(out)

	out /= 'mkdocs.yml'

	yml = YML.replace('{name}', name)

	for page in nav:
		yml += f'  - {page}: {nav[page]}\n'

	with open(out, 'w') as file:
		file.write(yml)


def main(args):
	nav = {}
	add_page(nav, Path('README.md'), 'README.md', 'Home')
	add_page(nav, Path('LICENSE'), 'LICENSE.md', 'License')

	gen_yml(args.name, nav)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate mkdocs')
	parser.add_argument('-n', '--name', type=str, help='package name', required=True)

	main(parser.parse_args())
