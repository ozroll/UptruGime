import sys
import os
import time

print("[Startup] Loading UpTru Engine modules...", flush=True)

try:
    from core.scraper import LeadDiscoveryEngine
    print("[Startup] Scraper loaded successfully.", flush=True)
except Exception as e:
    print(f"[Import Error - Scraper]: {e}", flush=True)

try:
    from core.generator import MetaAIGenerator
    print("[Startup] Generator loaded successfully.", flush=True)
except Exception as e:
    print(f"[Import Error - Generator]: {e}", flush=True)

try:
    from core.deployer import SiteDeployer
    print("[Startup] Deployer loaded successfully.", flush=True)
except Exception as e:
    print(f"[Import Error - Deployer]: {e}", flush=True)

def run_uptru_pipeline():
    print("==================================================")
    print("      UPTRU AUTONOMOUS B2B AGENCY ENGINE          ")
    print("==================================================", flush=True)
    
    start_time = time.time()

    # Step 1: Discover High-Priority Leads
    print("\n[Phase 1] Running Lead Discovery Engine...", flush=True)
    scraper = LeadDiscoveryEngine()
    targets = scraper.get_high_priority_targets()

    if not targets:
        print("[Info] No target leads found requiring a digital footprint.", flush=True)
        return

    # Step 2: Initialize Generator & Deployer
    generator = MetaAIGenerator()
    deployer = SiteDeployer()

    print(f"\n[Phase 2] Processing {len(targets)} target businesses through AI & Self-Correction Loop...", flush=True)

    successful_deployments = 0

    for lead in targets:
        name = lead.get("name")
        print(f"\n--------------------------------------------------", flush=True)
        print(f"Processing Target: {name} ({lead.get('category')})", flush=True)
        print(f"--------------------------------------------------", flush=True)

        # Generate & Validate HTML
        html_code = generator.generate_with_self_correction(lead)

        # Deploy Website
        file_path = deployer.deploy_site(name, html_code)

        if file_path:
            successful_deployments += 1

    elapsed = time.time() - start_time
    print("\n==================================================", flush=True)
    print(f"[Pipeline Complete] Successfully processed {successful_deployments}/{len(targets)} leads.", flush=True)
    print(f"Total Execution Time: {elapsed:.2f} seconds.", flush=True)
    print(f"Generated sites are saved in the 'generated_sites/' directory.", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    run_uptru_pipeline() 
