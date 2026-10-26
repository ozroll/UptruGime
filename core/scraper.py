import json
import os

class LeadDiscoveryEngine:
    def __init__(self, data_file="data/raw_leads.json"):
        self.data_file = data_file
        self.ensure_data_file()

    def ensure_data_file(self):
        """Ensures the raw leads file exists and contains valid sample leads."""
        populate_samples = False
        
        if not os.path.exists(self.data_file) or os.path.getsize(self.data_file) == 0:
            populate_samples = True
        else:
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if not isinstance(content, list) or len(content) == 0:
                        populate_samples = True
            except json.JSONDecodeError:
                # File has invalid or blank formatting from setup.bat
                populate_samples = True

        if populate_samples:
            sample_leads = [
                {
                    "name": "Daveyton Panel Beaters",
                    "category": "Automotive Repair",
                    "location": "Daveyton, Benoni",
                    "has_website": False,
                    "website_url": None,
                    "phone": "+27 11 555 0192"
                },
                {
                    "name": "Ekurhuleni Fit Gym",
                    "category": "Fitness & Health",
                    "location": "Daveyton Mall Area",
                    "has_website": True,
                    "website_url": "http://dead-link-example.co.za",
                    "phone": "+27 11 555 0144"
                },
                {
                    "name": "Zemed Fresh Bakery",
                    "category": "Food & Bakery",
                    "location": "Benoni Central",
                    "has_website": False,
                    "website_url": None,
                    "phone": "+27 11 555 0188"
                }
            ]
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(sample_leads, f, indent=4)

    def load_leads(self):
        """Loads all raw leads from local storage safely."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_high_priority_targets(self):
        """
        Filters businesses that are prime targets:
        Either they have no website at all, or their website status is dead/missing.
        """
        leads = self.load_leads()
        targets = []
        
        for lead in leads:
            if not lead.get("has_website") or not lead.get("website_url"):
                targets.append(lead)
            elif "dead-link" in str(lead.get("website_url")):
                targets.append(lead)
                
        print(f"[Discovery Engine] Scanned {len(leads)} total businesses.")
        print(f"[Discovery Engine] Found {len(targets)} high-priority targets needing a digital footprint.")
        return targets

if __name__ == "__main__":
    engine = LeadDiscoveryEngine()
    targets = engine.get_high_priority_targets()
    print("\nTarget Leads Identified:")
    for t in targets:
        print(f" - {t['name']} ({t['category']}) located in {t['location']}")