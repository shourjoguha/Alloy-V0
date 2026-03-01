# Hyrox Workout Scraper - Puppeteer MCP

Comprehensive scraper for Hyrox workouts from wodwell.com using Puppeteer MCP tools.

## Overview

This scraper extracts Hyrox workout data from wodwell.com with the following features:

- **Infinite Scroll**: Automatically scrolls to load all available workouts
- **Retry Logic**: Configurable retry attempts with exponential backoff
- **Intermediate Saves**: Saves progress every 10 workouts
- **Error Handling**: Comprehensive error tracking and logging
- **Progress Tracking**: Real-time progress updates and statistics
- **Target-Based**: Stops when target (200 workouts) is reached

## Target

- **Goal**: 200+ workouts for 80%+ coverage
- **Output**: `/Users/shourjosmac/Documents/Alloy V0/hyrox_workouts_scraped.json`

## Requirements

- Python 3.11+
- Puppeteer MCP server running
- Access to wodwell.com

## Installation

```bash
# Ensure Python 3.11+ is installed
python --version

# Install dependencies (if any needed)
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
cd /Users/shourjosmac/Documents/Alloy V0
python scripts/hyrox_scraper_puppeteer.py
```

### Configuration

Edit the following constants in `HyroxScraper` class:

```python
BASE_URL = "https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest"
OUTPUT_FILE = "/Users/shourjosmac/Documents/Alloy V0/hyrox_workouts_scraped.json"
TARGET_WORKOUTS = 200

# Retry and delay settings
retry_attempts = 3
retry_delay = 2
scroll_delay = 2
page_load_delay = 2
request_delay = 1
max_scrolls = 100
max_no_new_content = 5
```

## Output Format

The scraper saves results to `hyrox_workouts_scraped.json` with the following structure:

```json
{
  "scraped_at": "2026-02-28T12:00:00",
  "total_workouts": 200,
  "target_workouts": 200,
  "coverage_percentage": 100.0,
  "failed_urls": 5,
  "workouts": [
    {
      "url": "https://wodwell.com/wods/hyrox-workout-name",
      "wod_id": "hyrox-workout-name",
      "name": "Hyrox Workout Name",
      "description_lines": [
        "8km Run",
        "1000m Ski Erg",
        "50 Sled Push",
        "50 Sled Pull",
        "80 Burpee Broad Jumps",
        "1000m Row",
        "75 Wall Balls",
        "75 Overhead Walking Lunges",
        "100m Farmers Carry",
        "100 Sandbag Lunge",
        "75 Box Step-Overs"
      ],
      "workout_type": "Hyrox",
      "badge": "Endurance",
      "tags": ["Endurance", "Full Body", "Cardio"],
      "scraped_at": "2026-02-28T12:00:00"
    }
  ],
  "failed_urls_list": [
    {
      "url": "https://wodwell.com/wods/failed-workout",
      "attempts": 3,
      "failed_at": "2026-02-28T12:30:00"
    }
  ]
}
```

## Puppeteer MCP Integration

The scraper uses Puppeteer MCP tools for all browser operations. You need to integrate the actual MCP tools by replacing the placeholder methods in the `HyroxScraper` class:

### Required MCP Tool Methods

Replace the following methods with actual MCP tool calls:

#### 1. `_call_puppeteer_navigate(page, url: str)`

Navigate to a URL.

```python
async def _call_puppeteer_navigate(self, page, url: str) -> Dict[str, Any]:
    # Replace with actual MCP tool call
    # Example:
    result = await mcp_Puppeteer_puppeteer_navigate(url=url)
    return result
```

#### 2. `_call_puppeteer_evaluate(page, script: str, *args)`

Execute JavaScript in the page.

```python
async def _call_puppeteer_evaluate(self, page, script: str, *args) -> Dict[str, Any]:
    # Replace with actual MCP tool call
    # Example:
    result = await mcp_Puppeteer_puppeteer_evaluate(script=script)
    return result
```

#### 3. `_call_puppeteer_screenshot(page, path: str)`

Take a screenshot of the page.

```python
async def _call_puppeteer_screenshot(self, page, path: str) -> Dict[str, Any]:
    # Replace with actual MCP tool call
    # Example:
    result = await mcp_Puppeteer_puppeteer_screenshot(path=path)
    return result
```

#### 4. `_initialize_page()`

Initialize a new browser page.

```python
async def _initialize_page(self):
    # Replace with actual MCP tool call
    # Example:
    page = await mcp_Puppeteer_puppeteer_initialize()
    return page
```

#### 5. `_cleanup(page)`

Clean up resources and close the browser.

```python
async def _cleanup(self, page):
    # Replace with actual MCP tool call
    # Example:
    await mcp_Puppeteer_puppeteer_close(page)
```

## Workflow

1. **Initialize Browser**: Opens Puppeteer browser page
2. **Navigate to Base URL**: Loads `https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest`
3. **Infinite Scroll**: Scrolls to load all workouts (max 100 scrolls)
4. **Extract URLs**: Collects all workout page URLs
5. **Scrape Each Workout**: Visits each workout page and extracts data
6. **Save Results**: Saves to JSON file every 10 workouts
7. **Cleanup**: Closes browser and prints summary

## Error Handling

The scraper includes comprehensive error handling:

- **Retry Logic**: 3 attempts with exponential backoff (2s, 4s, 6s)
- **Failed URL Tracking**: All failed URLs are logged with timestamps
- **Intermediate Saves**: Progress is saved every 10 workouts
- **Graceful Degradation**: Continues scraping even if some workouts fail
- **Detailed Logging**: All errors are logged with stack traces

## Logging

Logs are output to console with the following format:

```
2026-02-28 12:00:00 - __main__ - INFO - Starting Hyrox Workout Scraper
2026-02-28 12:00:01 - __main__ - INFO - Navigating to https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest
2026-02-28 12:00:05 - __main__ - INFO - Successfully navigated to https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest
2026-02-28 12:00:05 - __main__ - INFO - Starting infinite scroll to load all workouts...
2026-02-28 12:00:10 - __main__ - INFO - Scroll 1/100: Found 25 workouts (+25 new)
2026-02-28 12:00:15 - __main__ - INFO - Scroll 2/100: Found 50 workouts (+25 new)
...
```

## Performance

- **Scroll Delay**: 2 seconds between scrolls
- **Page Load Delay**: 2 seconds after navigation
- **Request Delay**: 1 second between workout scrapes
- **Estimated Time**: ~5-10 minutes for 200 workouts (depending on network speed)

## Troubleshooting

### No workouts found

If no workout URLs are found:

1. Check if wodwell.com is accessible
2. Verify the page structure hasn't changed
3. Increase `max_scrolls` limit
4. Check browser console for JavaScript errors

### Scraping fails repeatedly

If scraping fails for multiple workouts:

1. Check network connectivity
2. Increase `retry_attempts` and `retry_delay`
3. Verify Puppeteer MCP server is running
4. Check for rate limiting by wodwell.com

### Incomplete data

If workout data is missing:

1. The page structure may have changed
2. Update the CSS selectors in `_extract_workout_data()`
3. Take a screenshot to debug the page structure

## Data Validation

After scraping, validate the data quality:

```bash
# Check number of workouts scraped
python -c "import json; data = json.load(open('hyrox_workouts_scraped.json')); print(f'Total: {data[\"total_workouts\"]}')"

# Check for missing names
python -c "import json; data = json.load(open('hyrox_workouts_scraped.json')); missing = [w for w in data['workouts'] if not w['name']]; print(f'Missing names: {len(missing)}')"

# Check for missing descriptions
python -c "import json; data = json.load(open('hyrox_workouts_scraped.json')); missing = [w for w in data['workouts'] if not w['description_lines']]; print(f'Missing descriptions: {len(missing)}')"
```

## Next Steps

After scraping:

1. **Validate Data**: Check data quality and completeness
2. **Load to Database**: Use existing loader scripts to import to PostgreSQL
3. **Process Workouts**: Parse workout descriptions for movements and exercises
4. **Generate Programs**: Use the scraped workouts to generate training programs

## Related Files

- `/Users/shourjosmac/Documents/Alloy V0/scripts/load_hyrox_workouts.py` - Load scraped data to database
- `/Users/shourjosmac/Documents/Alloy V0/docs/hyrox_staging_schema.md` - Database schema
- `/Users/shourjosmac/Documents/Alloy V0/config/program_config_enhanced.yaml` - Program configuration

## Notes

- Always be respectful when scraping (use appropriate delays)
- Check wodwell.com's terms of service before scraping
- The scraper is designed to be robust and handle various page structures
- Intermediate saves ensure data is not lost if the scraper crashes
