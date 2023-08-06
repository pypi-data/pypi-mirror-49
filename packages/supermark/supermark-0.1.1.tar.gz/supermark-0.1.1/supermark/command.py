import os
import click
from supermark import build

@click.command()
@click.option('-a', '--all', is_flag=True, default=False, help="Rebuild all pages, do not regard file timestamps.")
@click.option('-d', '--draft', is_flag=True, default=False, help="Also print draft parts of the documents.")
@click.option('-i', '--input', 'input', type=click.Path(exists=True), help='Input directory containing the source files.')
@click.option('-o', '--output', 'output', type=click.Path(exists=True), help='Output directory containing the source files.')
@click.option('-t', '--template', 'template', type=click.File('rb'), help='Template file for the transformation.')
def run(all, draft, input=None, output=None, template=None):
    input_path = input or os.path.join(os.getcwd(), 'pages')
    output_path = output or os.getcwd()
    template_path = template or os.path.join(os.getcwd(), 'templates/page.html')
    build(input_path, output_path, template_path, rebuild_all_pages=all, abort_draft= not draft)

