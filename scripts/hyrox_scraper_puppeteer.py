import json
import time
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any

class HyroxScraper:
    """Scraper for Hyrox workouts using Puppeteer MCP tool."""

    def __init__(self, max_workouts: int = 200, headless: bool = True):
        self.max_workouts = max_workouts
        self.headless = headless
        self.scraped_workouts = []
        self.errors = []
        self.failed_urls = []

    def scrape_workouts(self) -> List[Dict[str, Any]]:
        """Scrape Hyrox workouts from wodwell.com."""
        try:
            print("Starting Hyrox workout scraper...")
            print(f"Target: {self.max_workouts} workouts")
            
            # Navigate to Hyrox workouts page
            print("\n[1/4] Navigating to wodwell.com Hyrox workouts page...")
            workout_links = self._navigate_and_collect_links()
            print(f"✓ Found {len(workout_links)} workout links")

            if len(workout_links) == 0:
                print("✗ No workout links found. Exiting.")
                return []

            # Scrape each workout
            print(f"\n[2/4] Scraping workout details...")
            for i, link in enumerate(workout_links[:self.max_workouts], 1):
                print(f"\n[{i}/{min(len(workout_links), self.max_workouts)}] Scraping: {link['name']}")
                try:
                    workout = self._scrape_workout_details(link)
                    if workout:
                        self.scraped_workouts.append(workout)
                        print(f"  ✓ Scraped successfully ({len(workout.get('description_lines', []))} lines)")
                    else:
                        print(f"  ✗ Failed to scrape - returned None")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
                    self.errors.append({
                        'wod_id': link.get('wod_id'),
                        'name': link.get('name'),
                        'url': link.get('url'),
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
                    self.failed_urls.append(link.get('url'))

                # Intermediate save every 10 workouts
                if i % 10 == 0:
                    print(f"  💾 Intermediate save ({i} workouts)...")
                    self.save_results('hyrox_workouts_scraped_intermediate.json')

            print(f"\n[3/4] Scraping complete!")
            print(f"  ✓ Successfully scraped: {len(self.scraped_workouts)}")
            print(f"  ✗ Errors: {len(self.errors)}")

            return self.scraped_workouts

        except Exception as e:
            print(f"\n✗ Fatal error during scraping: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _navigate_and_collect_links(self) -> List[Dict[str, str]]:
        """Navigate to Hyrox workouts page and collect all workout links."""
        # Placeholder for Puppeteer MCP tool calls
        # In actual implementation, this would:
        # 1. Use mcp_Puppeteer_puppeteer_navigate to go to the URL
        # 2. Use mcp_Puppeteer_puppeteer_evaluate to extract workout links
        # 3. Use mcp_Puppeteer_puppeteer_screenshot for debugging if needed
        
        # For now, return sample data for testing
        return [
            {
                'wod_id': 'beverly-hills',
                'name': 'Beverly Hills',
                'url': 'https://wodwell.com/wod/beverly-hills/'
            },
            {
                'wod_id': 'chicago-2024',
                'name': 'Chicago 2024',
                'url': 'https://wodwell.com/wod/chicago-2024/'
            }
        ]

    def _scrape_workout_details(self, link: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Scrape details for a single workout."""
        try:
            # Placeholder for Puppeteer MCP tool calls
            # In actual implementation, this would:
            # 1. Use mcp_Puppeteer_puppeteer_navigate to go to the workout URL
            # 2. Use mcp_Puppeteer_puppeteer_evaluate to extract workout data
            # 3. Use mcp_Puppeteer_puppeteer_screenshot for debugging if needed
            
            # For now, return sample data for testing
            return {
                'wod_id': link['wod_id'],
                'name': link['name'],
                'url': link['url'],
                'description_lines': [
                    'Run 800m',
                    '30 burpees',
                    'Run 800m',
                    '30 burpees'
                ],
                'workout_type': 'for_time',
                'badge': None,
                'tags': ['hyrox'],
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"    Error scraping workout {link.get('wod_id')}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_results(self, output_file: str):
        """Save scraped workouts to JSON file."""
        results = {
            'workouts': self.scraped_workouts,
            'errors': self.errors,
            'failed_urls': self.failed_urls,
            'stats': {
                'total_scraped': len(self.scraped_workouts),
                'total_errors': len(self.errors),
                'total_failed_urls': len(self.failed_urls),
                'scraped_at': datetime.now().isoformat()
            }
        }

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"💾 Results saved to: {output_file}")

    def print_summary(self):
        """Print scraping summary."""
        print("\n" + "=" * 80)
        print("SCRAPING SUMMARY")
        print("=" * 80)
        print(f"Total workouts scraped: {len(self.scraped_workouts)}")
        print(f"Total errors: {len(self.errors)}")
        print(f"Failed URLs: {len(self.failed_urls)}")

        if self.scraped_workouts:
            workout_types = {}
            for workout in self.scraped_workouts:
                wtype = workout.get('workout_type', 'unknown')
                workout_types[wtype] = workout_types.get(wtype, 0) + 1

            print("\nWorkout types:")
            for wtype, count in sorted(workout_types.items()):
                print(f"  {wtype}: {count}")

            avg_lines = sum(len(w.get('description_lines', [])) for w in self.scraped_workouts) / len(self.scraped_workouts)
            print(f"\nAverage lines per workout: {avg_lines:.1f}")

        if self.errors:
            print("\nErrors (first 10):")
            for error in self.errors[:10]:
                print(f"  - {error['name']}: {error['error']}")

        if self.failed_urls:
            print("\nFailed URLs:")
            for url in self.failed_urls[:10]:
                print(f"  - {url}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scrape Hyrox workouts from wodwell.com')
    parser.add_argument('--output', '-o', default='hyrox_workouts_scraped.json',
                       help='Output JSON file (default: hyrox_workouts_scraped.json)')
    parser.add_argument('--max-workouts', '-m', type=int, default=200,
                       help='Maximum number of workouts to scrape (default: 200)')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode (default: True)')

    args = parser.parse_args()

    scraper = HyroxScraper(max_workouts=args.max_workouts, headless=args.headless)
    scraper.scrape_workouts()
    scraper.save_results(args.output)
    scraper.print_summary()


if __name__ == '__main__':
    main()
