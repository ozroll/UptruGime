import os
import re

class SiteDeployer:
    def __init__(self, output_dir="generated_sites"):
        self.output_dir = output_dir

    def slugify(self, text):
        """Converts business name into a clean folder/file slug."""
        text = text.lower().strip()
        text = re.sub(r'[\s\W_]+', '_', text)
        return text.strip('_')

    def deploy_site(self, lead_name, html_content):
        """
        Atomically deploys the verified website into an isolated folder.
        """
        slug = self.slugify(lead_name)
        client_dir = os.path.join(self.output_dir, slug)
        os.makedirs(client_dir, exist_ok=True)

        file_path = os.path.join(client_dir, "index.html")
        tmp_path = file_path + ".tmp"

        try:
            # Write atomically using a temporary file first to prevent corruption
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            os.rename(tmp_path, file_path)

            print(f"   [Deployer] Successfully deployed site for '{lead_name}' at: {file_path}", flush=True)
            return file_path
        except Exception as e:
            print(f"   [Deployer Error] Failed to deploy site for {lead_name}: {str(e)}", flush=True)
            return None

if __name__ == "__main__":
    deployer = SiteDeployer()
    test_html = "<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>"
    deployer.deploy_site("Test Business", test_html)
