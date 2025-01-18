#python concatenate_md.py --input_dir="S:\Moschip\Mardown_Sample_code\doc"
import argparse
import os
from pathlib import Path
from openai import OpenAI
import pypandoc
import panflute
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()


parser = argparse.ArgumentParser(description='Generate Markdown documentation from Python code using OpenAI or ast.')
parser.add_argument('--input_dir', help='The directory containing the Python code to document.', type=Path)
args = parser.parse_args()
print("*************************")
input_dir = args.input_dir
print(f"Input Path: {args.input_dir}")

def create_top_level_readme(file_contents):
    """
    Generate a top-level README.md file from multiple markdown files using OpenAI API.

    Args:
        file_contents (list of tuples): A list where each tuple contains a file name and its content.

    Returns:
        str: The generated README.md content.
    """
    # Combine file contents into a single prompt
    prompt = "Create a top-level markdown content that cross-link to the following markdown files:\n\n"
    for file_name, content in file_contents:
        prompt += f"{file_name}\n"
    prompt += "It must have Documentation Title and must have Description in it"

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that writes markdown files."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    return response.choices[0].message.content.replace("```markdown", "").replace("```","")

# Load your markdown files (example paths provided)
file_paths = []
file_contents = []


for file_path in input_dir.glob('**/*.md'):
    print(f"Processing file: {file_path}")
    relative_path = file_path.relative_to(input_dir.parent)
    file_paths.append(relative_path)
    with open(file_path, 'r') as file:
        file_contents.append((relative_path, file.read()))


# for path in file_paths:
#     with open(path, 'r') as file:
#         file_contents.append((path, file.read()))


index_readme = os.path.join(input_dir.parent,"README.md")
#Generate the README.md content
readme_content = create_top_level_readme(file_contents)

# Save the README.md file
with open(f"{index_readme}", "w") as readme_file:
    readme_file.write(readme_content)

print("README.md has been created!")
