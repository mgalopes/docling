from pathlib import Path
from docling.document_converter import DocumentConverter
from docling_core.types.doc import ImageRefMode

# Define the source document (URL or local path)
source = "https://arxiv.org/pdf/2408.09869"

# Initialize the DocumentConverter
converter = DocumentConverter()

# Convert the document
result = converter.convert(source)

# Define the output directory
output_dir = Path(r"C:\Users\garci\Downloads")
output_dir.mkdir(parents=True, exist_ok=True)

# Define the output Markdown file path
markdown_path = output_dir / "output.md"

# Export the document to Markdown with embedded images
result.document.save_as_markdown(markdown_path, image_mode=ImageRefMode.REFERENCED)

print(f"Markdown file with embedded images saved to: {markdown_path}")


#Explanation:
#ImageRefMode.EMBEDDED: This mode embeds images directly into the Markdown file as base64-encoded strings.
#ImageRefMode.REFERENCED: Alternatively, you can use this mode to save images as separate files and reference them in the Markdown.
# To do this, replace ImageRefMode.EMBEDDED with ImageRefMode.REFERENCED in the save_as_markdown method.