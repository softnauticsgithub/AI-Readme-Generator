from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

def generate_markdown_doc(api_key, python_code):
    """
    Generate markdown documentation for the given Python code using GPT.

    Args:
        api_key (str): OpenAI API key.
        python_code (str): The Python code to document.

    Returns:
        str: Markdown-formatted documentation.
    """

    # Prompt for GPT to generate markdown documentation
    prompt = f"""
    Generate detailed markdown documentation for the following Python code. Include a description, usage examples, and explanations for functions and classes:

    ```python
    {python_code}
    ```
    """

    try:
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
        return markdown_doc

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    # Example Python code
    example_code = '''
    def add(a, b):
        """Add two numbers and return the result."""
        return a + b

    class Calculator:
        """A simple calculator class."""
        
        def multiply(self, x, y):
            """Multiply two numbers."""
            return x * y
    '''

    # Replace with your OpenAI API key
    api_key = "your-openai-api-key"

    # Generate documentation
    markdown_documentation = generate_markdown_doc(api_key, example_code)
    print(markdown_documentation)
