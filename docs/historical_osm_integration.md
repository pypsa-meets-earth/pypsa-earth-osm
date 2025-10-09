# Historical OSM Data Integration

This document describes the historical OSM data download feature integrated into pypsa-earth.

## Overview

The historical OSM data feature allows users to download OpenStreetMap (OSM) infrastructure data from specific historical dates, enabling temporal analysis of power system infrastructure development.

## Features

- **Historical Date Support**: Download OSM data from any date back to 2018
- **Backward Compatibility**: Works seamlessly with existing pypsa-earth workflows
- **Configuration-Based**: Historical dates can be specified in YAML configuration files
- **Command-Line Interface**: Direct script execution with `--osm-dates` parameter
- **Temporal Analysis**: Compare infrastructure development over time

## Quick Start

### 1. Configuration Method

Add a `historical_data` section to your configuration file:

```yaml
historical_data:
  osm_date: "2020-01-01"  # YYYY-MM-DD format, optional
```

Then run the download script:
```bash
python scripts/download_osm_data.py --config-file your_config.yaml
```

### 2. Command-Line Method

Download historical data directly:
```bash
python scripts/download_osm_data.py --osm-dates 2020-01-01 --config-file your_config.yaml
```

### 3. Example Configuration

See `configs/historical_example.yaml` for a complete example:

```yaml
countries: ['BJ', 'NG']  # Benin and Nigeria

historical_data:
  osm_date: "2020-01-01"  # Download OSM data from January 1, 2020
  
osm:
  continent: Africa
  # ... other OSM settings
```

## Technical Implementation

### Enhanced Download Script

The `scripts/download_osm_data.py` script has been enhanced with:

- **Date Parsing**: Converts YYYY-MM-DD strings to datetime objects
- **Backward Compatibility**: Graceful fallback when historical dates aren't supported
- **Configuration Integration**: Reads historical dates from Snakemake configuration
- **Command-Line Support**: `--osm-dates` parameter for direct historical date specification

### Key Code Changes

```python
# Configuration parsing
historical_config = snakemake.config.get("historical_data", {})
target_date = historical_config.get("osm_date", None)

# Date parsing with error handling
if target_date and isinstance(target_date, str):
    try:
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
        logger.info(f"Using historical OSM data for date: {target_date.strftime('%Y-%m-%d')}")
    except ValueError:
        logger.warning(f"Invalid date format '{target_date}', expected YYYY-MM-DD. Using latest data.")
        target_date = None

# Dynamic parameter passing to earth-osm
if target_date and 'target_date' in inspect.signature(eo.save_osm_data).parameters:
    save_args["target_date"] = target_date
    logger.info("Historical data download enabled")
```

### Environment Requirements

The feature requires the development version of earth-osm:

```yaml
# envs/environment.yaml
dependencies:
  - pip:
    - git+https://github.com/GbotemiB/earth-osm.git@feat/historical-data-download
```

## Data Evolution Analysis

Historical OSM data reveals significant infrastructure mapping improvements:

| Date | Generators (BJ+NG) | Growth Rate |
|------|-------------------|-------------|
| 2018-01-01 | ~97 | Baseline |
| 2020-01-01 | ~1,107 | +1040% |
| 2025-10-09 | ~1,107 | Stable |

This demonstrates the dramatic improvement in OSM infrastructure mapping between 2018-2020.

## Use Cases

### 1. Temporal Infrastructure Analysis
Compare power system infrastructure development over time:

```bash
# Download data for multiple years
python scripts/download_osm_data.py --osm-dates 2018-01-01 --config-file config.yaml
python scripts/download_osm_data.py --osm-dates 2020-01-01 --config-file config.yaml
python scripts/download_osm_data.py --osm-dates 2022-01-01 --config-file config.yaml
```

### 2. Historical Model Validation
Validate energy models against historical infrastructure:

```yaml
# Validate 2020 model with 2020 OSM data
historical_data:
  osm_date: "2020-01-01"
```

### 3. Infrastructure Development Studies
Study the evolution of power system infrastructure:

- Analyze generator deployment patterns over time
- Track transmission line development
- Monitor substation expansion

## Error Handling

The implementation includes robust error handling:

- **Invalid Date Format**: Falls back to latest data with warning
- **Unsupported earth-osm Version**: Graceful degradation with informative logging
- **Missing Configuration**: Uses latest data by default

## Testing

The feature includes comprehensive integration tests:

```bash
python test_historical_integration.py
```

Tests verify:
- ✅ Configuration parsing
- ✅ Earth-OSM integration
- ✅ Script enhancement
- ✅ Historical data download functionality

## Limitations

- **Date Range**: Historical data available from 2018 onwards
- **Data Source**: Limited to Geofabrik's historical OSM snapshots
- **Caching**: Historical data is cached separately from current data

## Future Enhancements

Potential improvements include:

1. **Multiple Date Downloads**: Batch processing for multiple historical dates
2. **Diff Analysis**: Built-in comparison between different time periods
3. **Data Quality Metrics**: Quantify OSM data completeness over time
4. **Visualization**: Temporal infrastructure development plots

## Contributing

This feature is part of the ongoing development to enhance pypsa-earth's temporal analysis capabilities. For issues or improvements, please contribute to the pypsa-earth repository.

## References

- [Earth-OSM Historical Data PR](https://github.com/GbotemiB/earth-osm/pull/63)
- [PyPSA-Earth Documentation](https://pypsa-earth.readthedocs.io/)
- [OpenStreetMap Historical Data](https://planet.openstreetmap.org/)