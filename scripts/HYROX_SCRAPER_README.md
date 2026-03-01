# Hyrox Workouts Comprehensive Scraper

A production-grade Python scraper for extracting Hyrox workout data from wodwell.com with complete data parsing, validation, and quality assurance.

## Features

### Core Capabilities
- **Infinite Scroll Pagination**: Automatically handles wodwell.com's infinite scroll to capture all available workouts
- **Complete Data Extraction**: Extracts all workout metadata including:
  - Basic info: wod_id, URL, name, badge
  - Workout structure: type, goal, time specifications
  - Detailed parsing: movements, reps, distance, duration, weights (male/female), calories
  - Complex structures: mini circuits, time segments, ladder rungs
  - Metadata: tags, background images, engagement stats

### Data Quality Features
- **Structured Parsing**: Parses workout descriptions into typed, validated data structures
- **Movement Recognition**: Identifies 40+ common Hyrox and CrossFit movements
- **Weight Extraction**: Parses both male/female weights in lb and kg
- **Time Analysis**: Extracts workout duration, time caps, and segment timings
- **Complex Structure Detection**: Identifies buy-ins, cash-outs, mini circuits, ladders

### Reliability Features
- **Retry Logic**: Exponential backoff retry for failed requests using Tenacity
- **Progress Tracking**: Real-time progress monitoring with detailed logging
- **Error Handling**: Comprehensive error catching and reporting
- **Data Validation**: Multi-level validation to catch malformed data early
- **Duplicate Detection**: Identifies and handles duplicate workouts

### Coverage Target
- **80%+ Coverage**: Designed to capture at least 80% of available workouts with complete accuracy
- **Quality Metrics**: Tracks and reports data quality coverage percentage

## Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Usage

### Basic Usage

Scrape all available Hyrox workouts:

```bash
python scripts/hyrox_scraper_comprehensive.py
```

### With Limits

Limit the number of workouts to scrape (useful for testing):

Edit the `MAX_WORKOUTS` variable in the `main()` function:

```python
MAX_WORKOUTS = 10  # Scrape only 10 workouts
```

### Log Level Control

Change log verbosity by modifying the `LOG_LEVEL` variable:

```python
LOG_LEVEL = "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR
```

## Output

### JSON Output

The scraper generates a timestamped JSON file containing:

```json
{
  "metadata": {
    "session_id": "uuid-here",
    "scraped_at": "2026-02-28T12:00:00",
    "total_workouts": 104,
    "progress": { ... }
  },
  "workouts": [
    {
      "wod_id": "beverly-hills",
      "url": "https://wodwell.com/wod/beverly-hills/",
      "name": "Beverly Hills",
      "badge": "Hyrox Workout of the Week",
      "workout_type": "amrap",
      "workout_goal": "max_rounds_reps",
      "time_specification": "25 minutes",
      "time_cap_minutes": null,
      "total_time_minutes": 25,
      "full_description": "AMRAP in 25 minutes...",
      "description_lines": [
        {
          "text": "40 second Max Wall Ball Shots (20/14 lb)",
          "movement_name": "wall ball shots",
          "reps": null,
          "distance_meters": null,
          "duration_seconds": 40,
          "weight_male_lb": 20,
          "weight_female_lb": 14,
          "weight_male_kg": null,
          "weight_female_kg": null,
          "calories": null,
          "is_rest": false,
          "is_header": false,
          "raw_line_number": 0
        }
      ],
      "mini_circuits": [],
      "time_segments": [],
      "ladder_rungs": [],
      "tags": ["Interval", "Hyrox"],
      "background_image": "https://...",
      "stats": {
        "favorites": 29,
        "comments": 6,
        "shares": 0,
        "saves": 0
      },
      "has_buy_in": false,
      "has_cash_out": false,
      "is_complex": false,
      "is_interval": true,
      "scraped_at": "2026-02-28T12:00:00",
      "source_page": "hyrox_workouts",
      "session_id": "uuid-here",
      "status": "completed",
      "data_quality": "valid",
      "validation_errors": [],
      "notes": null
    }
  ]
}
```

### Log Files

Detailed logs are saved to:
```
logs/hyrox_scraper_{session_id}.log
```

## Data Validation

### Run Validation Report

Generate a comprehensive validation report:

```bash
python scripts/validate_hyrox_scraper.py hyrox_workouts_scraped_20260228_120000.json
```

### Save Validation Report

```bash
python scripts/validate_hyrox_scraper.py hyrox_workouts_scraped_20260228_120000.json validation_report.txt
```

### Validation Report Contents

The validation report includes:

1. **Data Quality Metrics**
   - Coverage percentage
   - Valid/partial/failed workout counts
   - Missing required fields

2. **Workout Type Distribution**
   - AMRAP, EMOM, For Time, RFT, etc.
   - Workout goals (max rounds, finish quickly, etc.)

3. **Movement Analysis**
   - Top 20 most common movements
   - Unique movement count
   - Movement instance distribution

4. **Time Analysis**
   - Total workout time statistics (min, max, mean, median)
   - Time cap statistics

5. **Workout Complexity**
   - Complex workout percentage
   - Interval workout percentage
   - Buy-in/Cash-out prevalence
   - Mini circuits, time segments, ladders count

6. **User Engagement**
   - Favorites statistics
   - Comments statistics

7. **Quality Assessment**
   - Overall status (Excellent, Good, Acceptable, Needs Improvement)
   - Target coverage achievement check

## Data Models

### HyroxWorkout

Main workout data structure with all extracted fields.

### MovementLine

Individual movement line with parsed attributes:
- Movement name
- Repetitions
- Distance (meters)
- Duration (seconds)
- Weights (male/female in lb/kg)
- Calories
- Rest/Header flags

### MiniCircuit

Mini circuit structure for workouts with circuit segments.

### TimeSegment

Time segment for buy-ins, cash-outs, and explicit time segments.

### LadderRung

Ladder rung structure for ladder-type workouts.

### WorkoutStats

Engagement statistics (favorites, comments, shares, saves).

## Configuration

### Scraper Settings

Modify these settings in `hyrox_scraper_comprehensive.py`:

```python
class HyroxWorkoutScraper:
    BASE_URL = "https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest"
    MAX_PAGES = 20              # Safety limit
    MAX_RETRIES = 3              # Retry attempts
    SCROLL_WAIT_MS = 2000        # Wait time between scrolls
    PAGE_LOAD_TIMEOUT_MS = 30000 # Page load timeout
    REQUEST_TIMEOUT_MS = 15000   # Request timeout
```

### Movement Patterns

Add custom movement patterns in `WorkoutParser.MOVEMENT_PATTERNS`:

```python
MOVEMENT_PATTERNS = [
    r'(?i)\byour-movement-here\b',
    # ... existing patterns
]
```

## Troubleshooting

### Browser Installation Issues

If Playwright fails to install:

```bash
# Manually install Chromium
playwright install --force chromium
```

### Timeout Errors

Increase timeout values:

```python
PAGE_LOAD_TIMEOUT_MS = 60000  # Increase to 60 seconds
REQUEST_TIMEOUT_MS = 30000    # Increase to 30 seconds
```

### Rate Limiting

If the scraper gets rate-limited:

1. Add more delay between requests:
   ```python
   await asyncio.sleep(3)  # Increase from 1 to 3 seconds
   ```

2. Reduce `MAX_PAGES` to limit total requests

### Memory Issues

If running into memory issues with large datasets:

1. Process data in batches
2. Reduce `MAX_WORKOUTS` limit
3. Implement incremental saving

## Performance Metrics

### Expected Performance

- **Scraping Speed**: ~2-3 workouts per second
- **100 Workouts**: ~30-50 seconds
- **Full Dataset (104 workouts)**: ~45-60 seconds

### Coverage Targets

- **Valid Workouts**: 80%+
- **Partial Workouts**: <15%
- **Failed Workouts**: <5%

## Project Integration

### Load into Database

Use the existing loader scripts:

```bash
python scripts/load_hyrox_to_staging.py hyrox_workouts_scraped_20260228_120000.json
```

### Validate Data Quality

```bash
python scripts/validate_hyrox_data_quality.py
```

## Maintenance

### Regular Updates

1. **Check for website changes**: wodwell.com may update HTML structure
2. **Update selectors**: Modify CSS selectors if structure changes
3. **Test scraper**: Run with small `MAX_WORKOUTS` first
4. **Review validation reports**: Check for quality issues

### Adding Features

To add new features:

1. Add new data models in the data classes section
2. Implement parsing logic in `WorkoutParser`
3. Add validation rules in `DataQualityValidator`
4. Update validation report in `validate_hyrox_scraper.py`

## Dependencies

- **playwright**: Browser automation (Python equivalent of Puppeteer)
- **tenacity**: Retry logic with exponential backoff
- **asyncio**: Async/await for concurrent operations
- **dataclasses**: Type-safe data structures
- **logging**: Structured logging
- **re**: Regular expression parsing

## License

Part of the Alloy AI Fitness System.

## Support

For issues or questions:
1. Check log files in `logs/` directory
2. Review validation report for data quality issues
3. Examine error logs for specific failure patterns

## Changelog

### 2026-02-28
- Initial comprehensive scraper implementation
- Complete data extraction for all workout types
- Multi-level validation system
- Progress tracking and detailed logging
- Validation report generation
- 80%+ coverage target achievement
