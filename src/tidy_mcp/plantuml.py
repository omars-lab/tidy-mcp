"""
Defalate impl based on:
- https://plantuml.com/text-encoding
- https://en.wikipedia.org/wiki/Deflate
- https://github.com/dougn/python-plantuml
- https://github.com/dougn/python-plantuml/blob/master/plantuml.py#L61-L66
Tool params based on:
- https://gofastmcp.com/servers/tools#parameter-metadata
"""

from typing import Annotated, Literal
from pydantic import Field

import base64
from zlib import compress
import string
import six

import requests
import os

if six.PY2:
    from string import maketrans
else:
    maketrans = bytes.maketrans

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))


def deflate_and_encode(plantuml_text):
    """zlib compress the plantuml text and encode it for the plantuml server.
    """
    zlibbed_str = compress(plantuml_text.strip().encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')

def tool_generate_plantuml_image_url(
    plantuml_content: 
        Annotated[str, Field(description="PlantUML compliant string of image we want to generate.")],
    format: 
        Annotated[
            Literal["uml", "png", "svg"], 
            Field(description="Output image format")
        ] = "svg"
) -> str:
    """
    Turns the plantuml (aka puml) content into a URL that can be used to generate an image.
    Returns/Output:
        A URL that can be used to generate an image.
    """
    return f'https://plantuml.com/plantuml/{format}/{deflate_and_encode(plantuml_content)}'

def tool_download_plantuml_image(
    image_url: Annotated[str, Field(description="URL of the image to download.")],
    file_path: Annotated[str, Field(description="Path to the file to save the image.")]
) -> str:
    """
    Downloads an image from a URL and saves it to a file.
    Handles redirects like curl -L to follow redirects properly.
    Returns/Output:
        The path to the saved image.
    """
    # Ensure the directory exists before attempting to save the file.
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        # Send a GET request to the URL with redirects enabled (like curl -L).
        # Add a `timeout` to prevent the script from hanging indefinitely.
        response = requests.get(image_url, timeout=10, allow_redirects=True)
        # Check if the request was successful (status code 200).
        response.raise_for_status()
        # Open the file in binary write mode and save the content.
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"image downloaded and saved successfully to '{file_path}'")
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")
        return None

def prompt_iterate_on_plantuml_diagram(
    plantuml_diagram_description: 
        Annotated[str, Field(description="Description of diagram we want to generate with PlantUML.")]
    ) -> str:
    return f"""
        You are tasked with generating a PlantUML diagram based on the following description: 
        ---
        ### Description of diagram
        {plantuml_diagram_description}
        ---
        
        ## Process Overview
        Follow this iterative process to generate and validate PlantUML diagrams:
        
        1. **Generate PlantUML Code**: Create clean, simple PlantUML syntax based on the description
        2. **Generate URL**: Use `tool_generate_plantuml_image_url` to create the PlantUML server URL
        3. **Download Diagram**: Use `tool_download_plantuml_image` to download the SVG (handles redirects automatically)
        4. **Validate Content**: Check the downloaded SVG for syntax errors or issues
        5. **Iterate if Needed**: If errors found, fix the PlantUML code and repeat
        
        ## Key Learnings from Previous Iterations
        
        ### PlantUML Best Practices:
        - Keep diagrams simple and focused
        - Use proper PlantUML syntax (actor, rectangle, arrows, notes)
        - Avoid complex nested structures that may cause parsing issues
        - Use clear, descriptive labels and titles
        
        ### Download Process:
        - The `tool_download_plantuml_image` function now handles redirects automatically (like `curl -L`)
        - PlantUML URLs often redirect (301/302), so redirects must be followed
        - Save files to `{os.environ.get('TMPDIR', '/tmp')}/tmp-puml.svg`
        - Check file size > 0 bytes to ensure successful download
        
        ### Validation Process:
        - Read the downloaded SVG file to check for syntax errors
        - Look for error messages in the SVG content
        - Verify the SVG contains actual diagram content, not just error text
        - Check that the file size is reasonable (> 1000 bytes for a simple diagram)
        
        ### Iteration Strategy:
        - If syntax errors found: Simplify the PlantUML code and try again
        - If download fails: Check URL format and try alternative approaches
        - If validation fails: Examine the SVG content for specific error messages
        - Maximum 3 iterations to avoid infinite loops
        
        ## Expected Output
        When successful, return:
        - Final working PlantUML URL
        - Confirmation of successful download
        - Brief description of the generated diagram
        - Any lessons learned during the iteration process
    """

if __name__ == "__main__":
    s = """
    @startuml
    Alice -> Bob: Hi!
    Bob --> Alice: Hello!
    @enduml
    """
    # Generate a proper URL using our function
    url = tool_generate_plantuml_image_url(s, "svg")
    print(f'Generated URL: {url}')
    print(f'Direct URL: https://plantuml.com/plantuml/uml/{deflate_and_encode(s)}')
    # Test downloading the image
    tool_download_plantuml_image(url, f"{os.environ.get('TMPDIR', '/tmp')}test.svg")
    