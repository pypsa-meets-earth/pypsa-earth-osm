#!/usr/bin/env python3
"""
Test script to verify the historical OSM data integration.
"""
import sys
from pathlib import Path
from datetime import datetime
import yaml

# Add the scripts directory to the path
sys.path.append('scripts')

def test_configuration_parsing():
    """Test that the historical configuration is parsed correctly."""
    
    # Load the historical configuration
    with open('configs/historical_example.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Check historical_data section exists
    assert 'historical_data' in config, "historical_data section missing from config"
    
    # Check osm_date is configured
    historical_config = config['historical_data']
    assert 'osm_date' in historical_config, "osm_date missing from historical_data"
    
    # Check date format
    osm_date_str = historical_config['osm_date']
    try:
        target_date = datetime.strptime(osm_date_str, "%Y-%m-%d")
        print(f"✓ Configuration parsing successful: {target_date.strftime('%Y-%m-%d')}")
        return True
    except ValueError:
        print(f"✗ Invalid date format: {osm_date_str}")
        return False

def test_earth_osm_integration():
    """Test that earth-osm library has target_date parameter."""
    try:
        import earth_osm.eo as eo
        import inspect
        
        # Check get_osm_data signature
        sig = inspect.signature(eo.get_osm_data)
        if 'target_date' in sig.parameters:
            print("✓ earth_osm.get_osm_data has target_date parameter")
        else:
            print("✗ earth_osm.get_osm_data missing target_date parameter")
            return False
            
        # Check save_osm_data signature
        sig = inspect.signature(eo.save_osm_data)
        if 'target_date' in sig.parameters:
            print("✓ earth_osm.save_osm_data has target_date parameter")
        else:
            print("✗ earth_osm.save_osm_data missing target_date parameter")
            return False
            
        return True
        
    except ImportError as e:
        print(f"✗ Could not import earth_osm: {e}")
        return False

def test_script_enhancement():
    """Test that the download script has been enhanced with historical support."""
    
    script_path = Path('scripts/download_osm_data.py')
    if not script_path.exists():
        print("✗ download_osm_data.py script not found")
        return False
    
    script_content = script_path.read_text()
    
    # Check for key historical data features
    checks = [
        ('datetime import', 'from datetime import datetime'),
        ('historical config parsing', 'historical_config = snakemake.config.get("historical_data", {})'),
        ('target_date extraction', 'target_date = historical_config.get("osm_date", None)'),
        ('date parsing logic', 'datetime.strptime(target_date, "%Y-%m-%d")'),
        ('target_date parameter passing', 'save_args["target_date"] = target_date')
    ]
    
    for check_name, check_string in checks:
        if check_string in script_content:
            print(f"✓ {check_name}: found")
        else:
            print(f"✗ {check_name}: missing")
            return False
    
    return True

def main():
    """Run all integration tests."""
    print("🧪 Testing Historical OSM Data Integration")
    print("=" * 50)
    
    tests = [
        ("Configuration Parsing", test_configuration_parsing),
        ("Earth-OSM Integration", test_earth_osm_integration),
        ("Script Enhancement", test_script_enhancement)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n🎯 Test Results Summary")
    print("=" * 50)
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        all_passed = all_passed and result
    
    if all_passed:
        print("\n🎉 All integration tests passed! Historical OSM data feature is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())