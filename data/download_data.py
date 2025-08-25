#!/usr/bin/env python3
"""
Download script for Ondoriya dataset from sample.ondoriya.com

Simple GET requests to fetch the CSV files needed for the lakehouse demo.
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm
from typing import Dict, List

# Base URL for dataset
BASE_URL = "https://sample.ondoriya.com"

# Essential files for regional insights demo
REQUIRED_FILES = {
    "regions.csv": "political_geography/regions.csv",
    "region_biome.csv": "political_geography/region_biome.csv", 
    "faction_distribution.csv": "political_geography/faction_distribution.csv",
    "people.csv": "core_demographics/people.csv",
    "households.csv": "core_demographics/households.csv"
}

def download_file(url: str, local_path: Path) -> bool:
    """Download a single file with progress bar."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Create parent directory if it doesn't exist
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download with progress bar
        with open(local_path, 'wb') as f, tqdm(
            desc=local_path.name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        
        return True
    except Exception as e:
        print(f"❌ Failed to download {local_path.name}: {e}")
        return False

def validate_files() -> bool:
    """Check if all required files exist and are not empty."""
    missing_files = []
    
    for filename, local_path in REQUIRED_FILES.items():
        full_path = Path("data") / local_path
        if not full_path.exists() or full_path.stat().st_size == 0:
            missing_files.append(filename)
    
    if missing_files:
        print(f"❌ Missing or empty files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present and non-empty")
    return True

def main():
    """Main download function."""
    print("🦆 Downloading Ondoriya Dataset")
    print("=" * 40)
    
    data_dir = Path("data")
    success_count = 0
    
    for filename, local_path in REQUIRED_FILES.items():
        print(f"\n📥 Downloading {filename}...")
        
        url = f"{BASE_URL}/{filename}"
        full_local_path = data_dir / local_path
        
        if download_file(url, full_local_path):
            success_count += 1
            print(f"✅ {filename} → {local_path}")
        else:
            print(f"❌ Failed: {filename}")
    
    print(f"\n📊 Download Summary")
    print("=" * 20)
    print(f"✅ Successful: {success_count}/{len(REQUIRED_FILES)}")
    print(f"❌ Failed: {len(REQUIRED_FILES) - success_count}/{len(REQUIRED_FILES)}")
    
    if success_count == len(REQUIRED_FILES):
        print("\n🎉 All files downloaded successfully!")
        
        # Validate files
        print("\n🔍 Validating files...")
        if validate_files():
            print("\n✅ Dataset ready for analysis!")
            print("Next steps:")
            print("  1. Run: jupyter notebook 01_eda/explore_ondoriya.ipynb")
            print("  2. Or: python demo_scripts/full_pipeline_demo.py")
        else:
            print("\n⚠️  Some files may be corrupted. Try downloading again.")
    else:
        print(f"\n❌ Download incomplete. Check your internet connection and try again.")

if __name__ == "__main__":
    main()