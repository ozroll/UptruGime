import bs4

class HTMLValidator:
    def __init__(self):
        pass

    def validate_html(self, html_content):
        """
        Inspects generated HTML content for structural integrity and styling hooks.
        Returns a tuple: (is_valid: bool, error_message: str)
        """
        if not html_content or not isinstance(html_content, str):
            return False, "Generated content is empty or not a string."

        # Check for basic HTML5 wrapper tags
        if "<html" not in html_content.lower() or "</html>" not in html_content.lower():
            return False, "Missing root <html> tags."
        
        if "<body" not in html_content.lower() or "</body>" not in html_content.lower():
            return False, "Missing <body> structural tags."

        try:
            # Parse with BeautifulSoup to catch severe syntax or parsing errors
            soup = bs4.BeautifulSoup(html_content, 'html.parser')
            
            # Verify critical elements exist
            if not soup.find('title'):
                return False, "SEO Failure: Missing <title> tag in the header."
            
            if not soup.find('body'):
                return False, "DOM Failure: BeautifulSoup could not parse a valid body element."

            # Check for Tailwind CSS CDN integration (essential for modern styling in our templates)
            html_text = str(soup)
            if "tailwindcss.com" not in html_text and "tailwind" not in html_text.lower():
                return False, "Styling Failure: Tailwind CSS CDN script tag is missing."

            return True, "Validation Passed Successfully."

        except Exception as e:
            return False, f"Parser Exception Error: {str(e)}"

if __name__ == "__main__":
    validator = HTMLValidator()
    
    # Test case 1: Valid HTML snippet
    valid_sample = """
    <!DOCTYPE html>
    <html lang="en">
    <head><title>Daveyton Panel Beaters</title>
    <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100">
        <h1 class="text-3xl font-bold">Welcome to Daveyton Panel Beaters</h1>
    </body>
    </html>
    """
    
    # Test case 2: Broken/Invalid HTML snippet
    invalid_sample = "<h1>Just a random string without tags</h1>"
    
    print("Testing Validator...")
    v1, msg1 = validator.validate_html(valid_sample)
    print(f"Sample 1 Result: {v1} | Message: {msg1}")
    
    v2, msg2 = validator.validate_html(invalid_sample)
    print(f"Sample 2 Result: {v2} | Message: {msg2}")
