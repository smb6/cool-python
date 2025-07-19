import os
from pathlib import Path
import click
from PyPDF2 import PdfReader, PdfWriter

@click.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output_dir', type=click.Path(file_okay=False))
@click.option('--password', prompt=True, hide_input=True, help='Password for the PDFs')
def batch_unlock_pdfs(input_dir, output_dir, password):
    """
    Walk through INPUT_DIR, unlock password-protected PDFs using PASSWORD,
    and save them to OUTPUT_DIR with 'OPEN' suffix added to filenames.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    unlocked_count = 0
    failed_files = []

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                input_file = Path(root) / file
                rel_path = input_file.relative_to(input_dir)
                output_file = output_dir / rel_path
                output_file = output_file.with_name(output_file.stem + "_OPEN.pdf")
                output_file.parent.mkdir(parents=True, exist_ok=True)

                try:
                    reader = PdfReader(str(input_file))
                    if reader.is_encrypted:
                        reader.decrypt(password)

                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)

                    with open(output_file, "wb") as f_out:
                        writer.write(f_out)

                    click.echo(f"Unlocked: {input_file} → {output_file}")
                    unlocked_count += 1

                except Exception as e:
                    click.echo(f"Failed: {input_file} ({e})", err=True)
                    failed_files.append(str(input_file))

    click.echo(f"\nSummary: {unlocked_count} files unlocked.")
    if failed_files:
        click.echo(f"{len(failed_files)} files failed to unlock.")
        for f in failed_files:
            click.echo(f"  - {f}")

if __name__ == '__main__':
    batch_unlock_pdfs()
g