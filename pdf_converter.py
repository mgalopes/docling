from pathlib import Path
import fitz  # PyMuPDF
from docling.document_converter import DocumentConverter
from docling_core.types.doc import ImageRefMode
import re
import shutil
import hashlib

# Define paths with raw strings for Windows
source = r"C:\Users\garci\Downloads\Lista de exercícios resolvidos 01 - Propriedades - PME3398.pdf"
output_dir = Path(r"C:\Users\garci\Downloads\Obsidian_Notes")
image_dir = output_dir / "attachments"

# Create directories if they don't exist
output_dir.mkdir(parents=True, exist_ok=True)
image_dir.mkdir(exist_ok=True)

# Get source filename components
source_stem = Path(source).stem
source_hash = hashlib.md5(source.encode()).hexdigest()[:6]  # Unique identifier

# Initialize converter and process document
converter = DocumentConverter()
result = converter.convert(source)
markdown_path = output_dir / f"{source_stem}.md"

# Save markdown with referenced images
result.document.save_as_markdown(
    markdown_path,
    image_mode=ImageRefMode.REFERENCED
)

# 1. Process automatically extracted images
image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
img_counter = 1

for file_path in output_dir.glob('**/*'):
    if file_path.suffix.lower() in image_extensions and file_path.is_file():
        # Generate unique filename with source reference
        new_name = f"{source_stem}_{source_hash}_img_{img_counter:03d}{file_path.suffix}"
        dest_path = image_dir / new_name
        
        # Handle duplicates
        while dest_path.exists():
            img_counter += 1
            new_name = f"{source_stem}_{source_hash}_img_{img_counter:03d}{file_path.suffix}"
            dest_path = image_dir / new_name
        
        shutil.move(str(file_path), str(dest_path))
        img_counter += 1

# 2. Capture PDF pages as fallback screenshots
doc = fitz.open(source)
total_pages = len(doc)  # Store page count before closing
screenshot_count = 0

for page_num in range(total_pages):
    # Generate unique image name with source reference
    img_name = f"{source_stem}_{source_hash}_page_{page_num+1:03d}.png"
    img_path = image_dir / img_name
    
    if not img_path.exists():
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=200)
        pix.save(str(img_path))
        screenshot_count += 1

doc.close()  # Close after all page operations

# 3. Update markdown references
with open(markdown_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace all image references
def replace_image_ref(match):
    alt_text = match.group(1)
    old_path = Path(match.group(2))
    return f"![[attachments/{source_stem}_{source_hash}_img_{old_path.stem}]]"

content = re.sub(
    r'!\[([^\]]*)\]\(((?:(?!attachments/).)*?)\)',
    replace_image_ref,
    content
)

# Add fallback screenshots using stored page count
if screenshot_count > 0:
    content += "\n\n## Document Pages\n"
    for page_num in range(total_pages):  # Use stored page count
        img_name = f"{source_stem}_{source_hash}_page_{page_num+1:03d}.png"
        content += f"\n![[attachments/{img_name}]]\n"

# Normalize paths and save
content = content.replace('\\', '/')
with open(markdown_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Markdown saved to: {markdown_path}")
print(f"Images saved to: {image_dir}")
print(f"Total images processed: {img_counter - 1}")
print(f"Fallback screenshots captured: {screenshot_count}")