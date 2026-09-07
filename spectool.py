"""
SpecTool
--------
Builds a single combined "spec book" PDF from a folder of individual
PDF files, and provides helper renaming utilities for files that use
a date-prefixed naming convention.

Filename convention expected by the rename helpers:
    "MMDDYY rest-of-name.pdf"   <-> "MM DD YY rest-of-name.pdf"

Example:
    "010524 Foo.pdf"  --(add spaces)-->  "01 05 24 Foo.pdf"
    "01 05 24 Foo.pdf" --(remove spaces)--> "010524 Foo.pdf"
"""

import logging
import os

from appJar import gui
from pypdf import PdfReader, PdfWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATE_PREFIX_LEN = 6  # "MMDDYY" -- six digits before spaces are inserted


def execute(_btn_name: str) -> None:
    """GUI button handler: reads the form, dispatches to the right action."""
    location = app.getEntry("location")
    action = app.option("Options")

    if not location:
        return app.popUp(
            "Empty Location", "Choose the directory with the files in it.", kind="warning"
        )

    if not os.path.isdir(location):
        return app.popUp(
            "Invalid Location", f'"{location}" is not a valid directory.', kind="error"
        )

    directory = os.listdir(location)

    if action == "Build Specs":
        errors = build_specs(location, directory)
        if errors:
            bad_files = "\n".join(f[:8] for f in errors)
            return app.popUp(
                "Some Files Failed",
                f"These files could not be read as PDFs (skipped):\n{bad_files}\n"
                "Please confirm they're valid PDFs and try again.",
                kind="warning",
            )
    elif action == "Add Spaces":
        rename_to_spaces(location, directory)
    elif action == "Remove Spaces":
        rename_no_spaces(location, directory)

    return app.infoBox("Done", "Done!")


def rename_to_spaces(location: str, directory: list[str]) -> None:
    """Turn 'MMDDYY name.pdf' into 'MM DD YY name.pdf'."""
    for filename in directory:
        prefix = filename[:DATE_PREFIX_LEN]
        if " " not in prefix and filename[:1].isdigit() and len(filename) >= DATE_PREFIX_LEN:
            new_filename = f"{filename[:2]} {filename[2:4]} {filename[4:6]}{filename[6:]}"
            os.rename(os.path.join(location, filename), os.path.join(location, new_filename))


def rename_no_spaces(location: str, directory: list[str]) -> None:
    """Turn 'MM DD YY name.pdf' back into 'MMDDYY name.pdf'."""
    for filename in directory:
        if filename[:1].isdigit() and len(filename) > 2 and filename[2] == " ":
            first_eight = filename[:8].replace(" ", "")
            rest = filename[8:]
            new_filename = first_eight + rest
            os.rename(os.path.join(location, filename), os.path.join(location, new_filename))


def build_specs(location: str, directory: list[str]) -> list[str]:
    """
    Merge every PDF in `directory` into CombinedSpecs.pdf, adding a
    blank page after any file with an odd page count (so each file's
    section starts on the same side of the sheet when printed), and
    bookmarking each file's starting page.

    Returns the list of filenames that could not be read as PDFs.
    """
    writer = PdfWriter()
    bookmarks: dict[str, int] = {}
    errors: list[str] = []
    page_count = 0

    for filename in directory:
        filepath = os.path.join(location, filename)
        logger.debug("Next file: %s", filename)

        try:
            reader = PdfReader(filepath, strict=False)
        except Exception as exc:
            logger.warning("Skipping %s (%s)", filename, exc)
            errors.append(filename)
            continue

        bookmarks[filename] = page_count

        for page in reader.pages:
            writer.add_page(page)
            page_count += 1

        if len(reader.pages) % 2 != 0:
            writer.add_blank_page()
            page_count += 1

    if errors:
        # Don't write a partial/incorrect combined file if anything failed.
        return errors

    for filename, start_page in bookmarks.items():
        writer.add_outline_item(filename, start_page)

    output_path = os.path.join(location, "CombinedSpecs.pdf")
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    return errors


if __name__ == "__main__":
    app = gui("SpecTool")
    app.font = 16
    app.setSticky("ew")
    app.setTitle("SpecTool")
    app.option("Options", ["Build Specs", "- Rename Files -", "Add Spaces", "Remove Spaces"])
    app.addDirectoryEntry("location")
    app.addButton("Start", execute)
    app.addButton("Quit", lambda _btn: app.stop())
    app.go()
