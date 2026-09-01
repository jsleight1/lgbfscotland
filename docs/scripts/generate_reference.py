"""Generate the code reference pages and navigation dynamically for a uv layout."""

from pathlib import Path
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

# Root points to the project root where pyproject.toml lives
root = Path(__file__).parent.parent.parent
# Points directly to the src directory
src = root / "src"

# Recursively loop through all Python files inside src/
for path in sorted(src.rglob("*.py")):
    # Extract the module path relative to 'src', ensuring the main folder name is kept
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    # Clean up __init__ files so they become the index of that directory
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    if not parts:
        continue

    nav[parts] = doc_path.as_posix()

    # Generate the Markdown file with the absolute dot-notation string
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        # This will correctly join your top-level package and modules (e.g., 'package.indicator')
        identifier = ".".join(parts)
        print(f"::: {identifier}", file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

# Save the generated navigation index inside the virtual reference directory
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
