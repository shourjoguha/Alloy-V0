"""
Hyrox Workouts Scraper using Puppeteer
Scrapes Hyrox workouts from wodwell.com and stores in staging tables
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.run(['pip', 'install', 'playwright'], check=True)
    subprocess.run(['playwright', 'install', 'chromium'], check=True)
    from playwright.async_api import async_playwright


class HyroxWorkoutScraper:
    """
    Scrapes Hyrox workouts from wodwell.com using Puppeteer
    """
    
    BASE_URL = "https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest"
    
    WORKOUT_TYPES = {
        'amrap': 'amrap',
        'emom': 'emom',
        'for time': 'for_time',
        'rounds for time': 'rounds_for_time',
        'rft': 'rounds_for_time',
        'buy-in': 'buy_in',
        'cash-out': 'cash_out',
        'time cap': 'time_cap',
        'ladder': 'ladder',
        'mini circuit': 'mini_circuit',
        'explicit time': 'explicit_time_guidance'
    }
    
    WORKOUT_GOALS = {
        'as many rounds as possible': 'max_rounds_reps',
        'as quickly as possible': 'finish_quickly',
        'finish as quickly as possible': 'finish_quickly',
        'complete all rounds': 'complete_rounds',
        'complete': 'complete_rounds',
        'build up to heaviest': 'max_load',
        'for load': 'max_load',
        'pace work': 'pace_work',
        'max effort': 'pace_work'
    }
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.workouts_scraped = 0
        self.errors_count = 0
        self.error_log = []
        
    async def scrape_all_workouts(self, max_workouts: int = None) -> List[Dict]:
        """
        Scrape all Hyrox workouts from the website
        
        Args:
            max_workouts: Maximum number of workouts to scrape (None for all)
            
        Returns:
            List of workout dictionaries
        """
        print(f"Starting Hyrox workout scraper (Session: {self.session_id})")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                workouts = []
                page_num = 1
                has_more = True
                
                while has_more:
                    print(f"Scraping page {page_num}...")
                    
                    url = f"{self.BASE_URL}&page={page_num}"
                    await page.goto(url, wait_until='networkidle', timeout=30000)
                    
                    page_workouts = await self._scrape_page(page, page)
                    workouts.extend(page_workouts)
                    
                    print(f"  Found {len(page_workouts)} workouts on page {page_num}")
                    print(f"  Total workouts scraped: {len(workouts)}")
                    
                    if max_workouts and len(workouts) >= max_workouts:
                        workouts = workouts[:max_workouts]
                        print(f"  Reached max_workouts limit: {max_workouts}")
                        has_more = False
                    else:
                        page_num += 1
                        
                        if len(page_workouts) == 0:
                            has_more = False
                        elif page_num > 10:
                            print("  Stopping after 10 pages to avoid excessive scraping")
                            has_more = False
                
                self.workouts_scraped = len(workouts)
                print(f"\nScraping complete! Total workouts: {len(workouts)}")
                
                return workouts
                
            except Exception as e:
                self.errors_count += 1
                self.error_log.append(f"Fatal error during scraping: {str(e)}")
                print(f"ERROR: {str(e)}")
                raise
            finally:
                await browser.close()
    
    async def _scrape_page(self, page, page_num: int) -> List[Dict]:
        """
        Scrape a single page of workouts
        
        Args:
            page: Playwright page object
            page_num: Page number
            
        Returns:
            List of workout dictionaries
        """
        try:
            workout_links = await page.query_selector_all('.wod-list a[href*="/wod/"]')
            
            if not workout_links:
                return []
            
            workouts = []
            for link in workout_links:
                workout = await self._parse_workout_card(link)
                if workout:
                    workouts.append(workout)
            
            return workouts
            
        except Exception as e:
            self.errors_count += 1
            self.error_log.append(f"Error scraping page {page_num}: {str(e)}")
            print(f"  Error scraping page {page_num}: {str(e)}")
            return []
    
    async def _parse_workout_card(self, link) -> Optional[Dict]:
        """
        Parse a workout card HTML element
        
        Args:
            link: Playwright element handle for workout card link
            
        Returns:
            Workout dictionary or None if parsing failed
        """
        try:
            workout = {}
            
            workout['url'] = await link.get_attribute('href')
            
            wod_id_match = re.search(r'/wod/([a-z0-9-]+)/', workout['url'])
            workout['wod_id'] = wod_id_match.group(1) if wod_id_match else None
            
            name_el = await link.query_selector('h2')
            workout['name'] = await name_el.inner_text() if name_el else ''
            
            badge_el = await link.query_selector('[class*="badge-text"]')
            workout['badge'] = await badge_el.inner_text() if badge_el else None
            
            description_container = await link.query_selector('[class*="wod-description"] p[class*="workout"]')
            if description_container:
                description_text = await description_container.inner_text()
                workout['full_description'] = description_text
                
                workout['workout_type'] = self._extract_workout_type(description_text)
                workout['workout_goal'] = self._extract_workout_goal(description_text)
                workout['time_specification'] = self._extract_time_specification(description_text)
                workout['total_time_minutes'] = self._extract_total_minutes(description_text)
                workout['time_cap_minutes'] = self._extract_time_cap(description_text)
                workout['has_buy_in'] = 'buy-in' in description_text.lower()
                workout['has_cash_out'] = 'cash-out' in description_text.lower()
                workout['is_complex'] = self._detect_complex_workout(description_text)
                
                workout['description_lines'] = self._parse_description_text(description_text)
            else:
                workout['full_description'] = ''
                workout['workout_type'] = 'unknown'
                workout['workout_goal'] = 'unknown'
                workout['time_specification'] = None
                workout['total_time_minutes'] = None
                workout['time_cap_minutes'] = None
                workout['has_buy_in'] = False
                workout['has_cash_out'] = False
                workout['is_complex'] = False
                workout['description_lines'] = []
            
            tags_el = await link.query_selector('[class*="wod-terms"], [class*="tag"]')
            if tags_el:
                tag_elements = await tags_el.query_selector_all('a, span')
                tags = []
                for tag in tag_elements:
                    text = await tag.inner_text()
                    if text and len(text.strip()) < 50:
                        tags.append(text.strip())
                workout['tags'] = tags
            else:
                workout['tags'] = ['hyrox']
            
            bg_image_el = await link.query_selector('[class*="namesake-wod-preview"][style*="background-image"]')
            if bg_image_el:
                style = await bg_image_el.get_attribute('style')
                url_match = re.search(r"url\(['\"]?([^'\"]+)['\"]?\)", style or '')
                workout['background_image'] = url_match.group(1) if url_match else None
            else:
                workout['background_image'] = None
            
            stats_el = await link.query_selector('[data-id]')
            if stats_el:
                workout['stats'] = await self._parse_stats(stats_el)
            else:
                workout['stats'] = {'favorites': 0, 'comments': 0}
            
            workout['scraped_at'] = datetime.now().isoformat()
            workout['source_page'] = 'hyrox_workouts'
            workout['status'] = 'pending_review'
            workout['validation_errors'] = None
            workout['notes'] = None
            
            return workout
            
        except Exception as e:
            self.errors_count += 1
            error_msg = f"Error parsing workout card: {str(e)}"
            self.error_log.append(error_msg)
            print(f"    {error_msg}")
            return None
    
    async def _parse_stats(self, stats_el) -> Dict:
        """
        Parse workout statistics (favorites, comments)
        
        Args:
            stats_el: Playwright element handle for stats container
            
        Returns:
            Dictionary with 'favorites' and 'comments' counts
        """
        try:
            favorites_el = await stats_el.query_selector('[class*="favorite"], [class*="fav"]')
            comments_el = await stats_el.query_selector('[class*="comment"]')
            
            favorites = 0
            comments = 0
            
            if favorites_el:
                fav_text = await favorites_el.inner_text()
                fav_match = re.search(r'(\d+)', fav_text)
                favorites = int(fav_match.group(1)) if fav_match else 0
            
            if comments_el:
                comment_text = await comments_el.inner_text()
                comment_match = re.search(r'(\d+)', comment_text)
                comments = int(comment_match.group(1)) if comment_match else 0
            
            return {'favorites': favorites, 'comments': comments}
            
        except Exception:
            return {'favorites': 0, 'comments': 0}
    
    def _extract_workout_type(self, text: str) -> str:
        """
        Extract workout type from description text
        
        Args:
            text: Workout description text
            
        Returns:
            Workout type enum value
        """
        text_lower = text.lower()
        
        for pattern, workout_type in self.WORKOUT_TYPES.items():
            if pattern in text_lower:
                return workout_type
        
        return 'unknown'
    
    def _extract_workout_goal(self, text: str) -> str:
        """
        Extract workout goal from description text
        
        Args:
            text: Workout description text
            
        Returns:
            Workout goal enum value
        """
        text_lower = text.lower()
        
        for pattern, goal in self.WORKOUT_GOALS.items():
            if pattern in text_lower:
                return goal
        
        return 'unknown'
    
    def _extract_time_specification(self, text: str) -> Optional[str]:
        """
        Extract time specification from description text
        
        Args:
            text: Workout description text
            
        Returns:
            Time specification string or None
        """
        time_patterns = [
            r'(\d+)\s*min(?:ute)?s?',
            r'(\d+):(\d+)',
            r'(\d+)\s*hours?',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_total_minutes(self, text: str) -> Optional[int]:
        """
        Extract total workout time in minutes
        
        Args:
            text: Workout description text
            
        Returns:
            Total minutes or None
        """
        minutes_match = re.search(r'(\d+)\s*min(?:ute)?s?', text, re.IGNORECASE)
        if minutes_match:
            return int(minutes_match.group(1))
        
        time_match = re.search(r'(\d+):(\d+)', text)
        if time_match:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            return hours * 60 + minutes
        
        return None
    
    def _extract_time_cap(self, text: str) -> Optional[int]:
        """
        Extract time cap in minutes
        
        Args:
            text: Workout description text
            
        Returns:
            Time cap minutes or None
        """
        cap_patterns = [
            r'time\s*cap\s*[:\s]*(\d+)\s*min(?:ute)?s?',
            r'cap\s*[:\s]*(\d+)\s*min(?:ute)?s?',
        ]
        
        for pattern in cap_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _detect_complex_workout(self, text: str) -> bool:
        """
        Detect if workout has complex structure (mini circuits, ladders, etc.)
        
        Args:
            text: Workout description text
            
        Returns:
            True if workout is complex
        """
        complex_indicators = [
            'mini circuit',
            'ladder',
            'time segment',
            'then',
            'after that',
            'followed by',
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in complex_indicators)
    
    def _parse_description_text(self, text: str) -> List[Dict]:
        """
        Parse description text into structured lines
        
        Args:
            text: Workout description text
            
        Returns:
            List of line dictionaries
        """
        lines = text.split('\n')
        parsed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parsed_line = {
                'text': line,
                'is_header': any(indicator in line.lower() for indicator in ['round', 'complete', 'for time', 'amrap', 'emom']),
                'movement': self._extract_movement_name(line),
                'reps': self._extract_reps(line),
                'distance': self._extract_distance(line),
                'duration': self._extract_duration(line),
                'weight': self._extract_weight(line),
                'calories': self._extract_calories(line)
            }
            
            parsed_lines.append(parsed_line)
        
        return parsed_lines
    
    def _extract_movement_name(self, text: str) -> Optional[str]:
        """
        Extract movement name from text
        
        Args:
            text: Text to parse
            
        Returns:
            Movement name or None
        """
        movements = [
            'wall ball shots', 'ski erg', 'lunges', 'burpees', 'v-ups',
            'run', 'row', 'sandbag lunges', 'hand release push-ups',
            'farmer\'s carry', 'sit-ups', 'push-ups', 'pull-ups',
            'kettlebell swings', 'box jumps', 'double unders', 'squat cleans',
            'deadlifts', 'thrusters', 'toes to bar', 'chest to bar',
            'muscle-ups', 'power cleans', 'snatches'
        ]
        
        text_lower = text.lower()
        for movement in movements:
            if movement in text_lower:
                return movement
        
        return None
    
    def _extract_reps(self, text: str) -> Optional[int]:
        """
        Extract repetitions from text
        
        Args:
            text: Text to parse
            
        Returns:
            Repetition count or None
        """
        patterns = [
            r'^(\d+)\s+(?!meter|cal|lb|kg)',
            r'(\d+)\s+reps?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_distance(self, text: str) -> Optional[int]:
        """
        Extract distance from text
        
        Args:
            text: Text to parse
            
        Returns:
            Distance in meters or None
        """
        match = re.search(r'(\d+)\s*meters?\s*(run|row)?', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        return None
    
    def _extract_duration(self, text: str) -> Optional[int]:
        """
        Extract duration from text
        
        Args:
            text: Text to parse
            
        Returns:
            Duration in seconds or None
        """
        patterns = [
            r'(\d+)\s*sec(?:ond)?s?',
            r'(\d+):(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return int(match.group(1)) * 60 + int(match.group(2))
                return int(match.group(1))
        
        return None
    
    def _extract_weight(self, text: str) -> Optional[Dict]:
        """
        Extract weight from text
        
        Args:
            text: Text to parse
            
        Returns:
            Dictionary with 'value' and 'unit' or None
        """
        match = re.search(r'(\d+)\s*(lb|kg)', text, re.IGNORECASE)
        if match:
            return {'value': int(match.group(1)), 'unit': match.group(2).lower()}
        
        return None
    
    def _extract_calories(self, text: str) -> Optional[int]:
        """
        Extract calories from text
        
        Args:
            text: Text to parse
            
        Returns:
            Calorie count or None
        """
        match = re.search(r'(\d+)\s*cal(?:ories)?', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        return None
    
    def get_scrape_summary(self) -> Dict:
        """
        Get summary of scraping session
        
        Returns:
            Dictionary with summary information
        """
        return {
            'session_id': self.session_id,
            'workouts_saved': self.workouts_scraped,
            'errors_count': self.errors_count,
            'error_summary': '\n'.join(self.error_log[:10]) if self.error_log else None
        }


async def main():
    """
    Main entry point for Hyrox scraper
    """
    print("=" * 60)
    print("HYROX WORKOUTS SCRAPER")
    print("=" * 60)
    
    scraper = HyroxWorkoutScraper()
    
    try:
        workouts = await scraper.scrape_all_workouts(max_workouts=5)
        
        print("\n" + "=" * 60)
        print("SCRAPING SUMMARY")
        print("=" * 60)
        summary = scraper.get_scrape_summary()
        print(f"Session ID: {summary['session_id']}")
        print(f"Workouts scraped: {summary['workouts_saved']}")
        print(f"Errors: {summary['errors_count']}")
        
        if summary['error_summary']:
            print(f"\nError Summary:\n{summary['error_summary']}")
        
        print("\n" + "=" * 60)
        print("SAMPLE WORKOUTS (first 3)")
        print("=" * 60)
        for i, workout in enumerate(workouts[:3], 1):
            print(f"\n{i}. {workout.get('name', 'Unknown')}")
            print(f"   Type: {workout.get('workout_type')}")
            print(f"   URL: {workout.get('url')}")
            print(f"   Lines: {len(workout.get('description_lines', []))}")
        
        output_file = f"hyrox_workouts_scraped_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(workouts, f, indent=2)
        
        print(f"\nData saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
