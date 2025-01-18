#python S:\Moschip\openai-quickstart-python\examples\assistant-basic\python_large_doc_generators.py --input_dir="S:\Moschip\Mardown_Sample_code\src" --output_dir="S:\Moschip\Mardown_Sample_code\doc"
import argparse
import os
from pathlib import Path
import time
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

CHUNK_SIZE = 2000  # OpenAI's token limit

def validate_file(code_file):
    if not os.path.isfile(code_file):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(code_file))
    return code_file

class DocumentationGenerator:
    """
    """
    def __init__(self, use_openai=True):
        self.use_openai = use_openai

    def generate_documentation(self, code_chunk):
        """
        Given a chunk of Python code, use GPT-3 to generate an explanation.
        """
        # Prompt for GPT to generate markdown documentation
        prompt = f"""
        Generate detailed markdown documentation for the following Python code. Include a description, usage examples, and explanations for functions and classes:

        ```python
        {code_chunk}
        ```
        """
        markdown_doc = ""
        try:
            if self.use_openai:
                time.sleep(10)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates markdown documentation for Python code."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=1500
                )

                # Extract the content of the response
                markdown_doc = response.choices[0].message.content
                # return markdown_doc
            else:
                # Placeholder for another documentation generation method
                return "Not implemented"
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            return markdown_doc
    
    def generate_markdown_to_html(self, markdown_text):
        """
        Convert Markdown file to HTML file
        """
        # Prompt for GPT to generate markdown documentation
        prompt = f"Convert the following Markdown content to HTML:\n\n{markdown_text}"
        markdown_html = ""
        try:
            if self.use_openai:
                time.sleep(10)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that convert markdown documentation to HTML"},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=1500,
                    temperature=0   # For deterministic output
                )

                # Extract the content of the response
                markdown_html = response.choices[0].message.content
                # return markdown_doc
            else:
                # Placeholder for another documentation generation method
                return "Not implemented"
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            return markdown_html
    
    def generate_chunked_html(self, file_content):
        """
        Handle the creation of documentation for large files.
        """
        chunks = [file_content[i:i + CHUNK_SIZE] for i in range(0, len(file_content), CHUNK_SIZE)]
        print(f"Generating draft documentation for a file with {len(chunks)} chunks.")
        # Refinement
        md_to_html = "".join([self.generate_markdown_to_html(chunk) + "\n\n" for chunk in chunks])
        return md_to_html

    def generate_chunked_documentation(self, file_content):
        """
        Handle the creation of documentation for large files.
        """
        chunks = [file_content[i:i + CHUNK_SIZE] for i in range(0, len(file_content), CHUNK_SIZE)]

        print(f"Generating draft documentation for a file with {len(chunks)} chunks.")

        # Refinement
        refined_documentation = "".join([self.generate_documentation(chunk) + "\n\n" for chunk in chunks])
        

        return refined_documentation

    def create_top_level_readme(self, file_contents):
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
        time.sleep(10)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that writes markdown files."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )

        return response.choices[0].message.content.replace("```markdown", "").replace("```","")

    def convert_md_html(self, output_dir: Path):
        """
        Convert Markdown to HTML
        """
        # generate md file to HTML file
        for file_path in output_dir.glob('**/*.md'):
            print(f"Processing file: {file_path}")
            with open(file_path, 'r') as file:
                file_content = file.read()
                doc = self.generate_chunked_html(file_content)

                # Output file in the output directory with same folder structure
                # output_path = os.path.join(output_dir, file_path.relative_to(output_dir).with_suffix('.html'))
                # output_dir.parent.mkdir(parents=True, exist_ok=True)

                output_path = output_dir / file_path.relative_to(output_dir).with_suffix('.html')
                output_path.parent.mkdir(parents=True, exist_ok=True)

                print(f"Writing documentation to: {output_path}")
                with open(output_path, 'w') as out_file:
                    out_file.write(doc)

    def generate_index_readme(self, doc_dir:Path):
        """
        Top Level Index file
        """
        # Load your markdown files
        file_paths = []
        file_contents = []
        for file_path in doc_dir.glob('**/*.md'):
            print(f"Processing file: {file_path}")
            relative_path = file_path.relative_to(doc_dir.parent)
            file_paths.append(relative_path)
            with open(file_path, 'r') as file:
                file_contents.append((relative_path, file.read()))
        
        index_readme = os.path.join(doc_dir.parent,"README.md")
        #Generate the README.md content
        readme_content = self.create_top_level_readme(file_contents)

        # Save the README.md file
        with open(f"{index_readme}", "w", encoding="utf-8") as readme_file:
            readme_file.write(readme_content)

        print("README.md has been created!")



    def process_directory(self, input_dir: Path, output_dir: Path):
        """
        Walks the input directory and processes each Python file found.
        """
        for file_path in input_dir.glob('**/*.py'):
            print(f"Processing file: {file_path}")
            with open(file_path, 'r') as file:
                file_content = file.read()
                doc = self.generate_chunked_documentation(file_content)

                # Output file in the output directory with same folder structure
                #output_path = os.path.join(output_dir, file_path.relative_to(input_dir).with_suffix('.md'))

                output_path = output_dir / file_path.relative_to(input_dir).with_suffix('.md')
                output_path.parent.mkdir(parents=True, exist_ok=True)

                #output_dir.parent.mkdir(parents=True, exist_ok=True)

                print(f"Writing documentation to: {output_path}")
                with open(output_path, 'w', encoding="utf-8") as out_file:
                    out_file.write(doc)
        
    
    def process_file(self, input_dir: Path, output_dir: Path):
        """
        Walks the input directory and processes each Python file found.
        """
        for file_path in input_dir.glob('**/*.py'):
            print(f"Processing file: {file_path}")
            with open(file_path, 'r') as file:
                file_content = file.read()
                doc = self.generate_chunked_documentation(file_content)

                # Output file in the output directory with same folder structure
                #output_path = os.path.join(output_dir, file_path.relative_to(input_dir).with_suffix('.md'))

                output_path = output_dir / file_path.relative_to(input_dir).with_suffix('.md')
                output_path.parent.mkdir(parents=True, exist_ok=True)

                #output_dir.parent.mkdir(parents=True, exist_ok=True)

                print(f"Writing documentation to: {output_path}")
                with open(output_path, 'w', encoding="utf-8") as out_file:
                    out_file.write(doc)

    def process_one_file(self, input_file, output_dir: Path):
        """
        Generate doc for only one file
        """
        input_file_path=Path(input_file)
        print(f"Processing file: {input_file_path}")
        with open(input_file_path, 'r') as file:
            file_content = file.read()
            doc = self.generate_chunked_documentation(file_content)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = os.path.join(output_dir, os.path.basename(input_file_path.with_suffix('.md')))
            print(output_path)
            print(f"Writing documentation to: {output_path}")
            with open(output_path, 'w', encoding="utf-8") as out_file:
                out_file.write(doc)


def main():
    parser = argparse.ArgumentParser(description='Generate Markdown documentation from Python code using OpenAI or ast.')
    parser.add_argument('--input_dir', help='The directory containing the Python code to document.', type=Path)
    parser.add_argument('--output_dir', help='The directory to write the Markdown files to.',type=Path, required=True)
    parser.add_argument("--input_code_file", required=False, type=validate_file, help="Single code file path to generate a doc", metavar="FILE")
    args = parser.parse_args()
   
    print("*************************")
    input_dir = args.input_dir
    output_dir = args.output_dir
    single_code_file = args.input_code_file
    print(f"Input Path: {args.input_dir}")
    print(f"Output Path: {args.output_dir}")
    print(f"Single filep path: {args.input_code_file}")

    if input_dir is not None and input_dir.is_dir():
        print("In..")
        output_dir.mkdir(parents=True, exist_ok=True)
        doc_generator = DocumentationGenerator()
        doc_generator.process_directory(input_dir, output_dir)
        print("****************** Readme files has generated. ***************")
        doc_generator.generate_index_readme(doc_dir=output_dir)
        print("****************** Index README file is also available ***************")
    
    if single_code_file is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        doc_generator = DocumentationGenerator()
        doc_generator.process_one_file(input_file=single_code_file, output_dir=output_dir)
        


if __name__ == "__main__":
    main()