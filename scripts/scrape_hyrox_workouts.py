"""
Hyrox Workouts Scraper
Scrapes Hyrox workouts from wodwell.com and stores in staging tables
"""

import asyncio
import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


class HyroxWorkoutScraper:
    """
    Scrapes Hyrox workouts from wodwell.com
    """
    
    BASE_URL = "https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest"
    
    WORKOUT_TYPES = {
        'amrap': 'amrap',
        'emom': 'emom',
        'for time': 'for_time',
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
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            },
            timeout=30.0,
            follow_redirects=True
        )
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
        
        try:
            workouts = []
            page = 1
            has_more = True
            
            while has_more:
                print(f"Scraping page {page}...")
                page_workouts, has_more = await self._scrape_page(page)
                workouts.extend(page_workouts)
                
                print(f"  Found {len(page_workouts)} workouts on page {page}")
                print(f"  Total workouts scraped: {len(workouts)}")
                
                if max_workouts and len(workouts) >= max_workouts:
                    workouts = workouts[:max_workouts]
                    print(f"  Reached max_workouts limit: {max_workouts}")
                    has_more = False
                else:
                    page += 1
                    
                    if page > 10:
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
    
    async def _scrape_page(self, page: int) -> tuple[List[Dict], bool]:
        """
        Scrape a single page of workouts
        
        Args:
            page: Page number
            
        Returns:
            Tuple of (workouts list, has_more boolean)
        """
        url = f"{self.BASE_URL}&page={page}"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            workout_cards = soup.select('.wod-list a[href*="/wod/"]')
            
            if not workout_cards:
                return [], False
            
            workouts = []
            for card in workout_cards:
                workout = await self._parse_workout_card(card)
                if workout:
                    workouts.append(workout)
            
            has_more = len(workout_cards) > 0
            
            return workouts, has_more
            
        except Exception as e:
            self.errors_count += 1
            self.error_log.append(f"Error scraping page {page}: {str(e)}")
            print(f"  Error scraping page {page}: {str(e)}")
            return [], False
    
    async def _parse_workout_card(self, card) -> Optional[Dict]:
        """
        Parse a workout card HTML element
        
        Args:
            card: BeautifulSoup element for workout card
            
        Returns:
            Workout dictionary or None if parsing failed
        """
        try:
            workout = {}
            
            workout['url'] = card.get('href', '').strip()
            
            wod_id_match = re.search(r'/wod/([a-z0-9-]+)/', workout['url'])
            workout['wod_id'] = wod_id_match.group(1) if wod_id_match else None
            
            name_el = card.select_one('h2')
            workout['name'] = name_el.get_text().strip() if name_el else ''
            
            badge_el = card.select_one('[class*="badge-text"]')
            workout['badge'] = badge_el.get_text().strip() if badge_el else None
            
            description_container = card.select_one('[class*="wod-description"] p[class*="workout"]')
            if description_container:
                description_text = description_container.get_text('\n', strip=True)
                workout['full_description'] = description_text
                
                workout['workout_type'] = self._extract_workout_type(description_text)
                workout['workout_goal'] = self._extract_workout_goal(description_text)
                workout['time_specification'] = self._extract_time_specification(description_text)
                workout['total_time_minutes'] = self._extract_total_minutes(description_text)
                workout['time_cap_minutes'] = self._extract_time_cap(description_text)
                workout['has_buy_in'] = 'buy-in' in description_text.lower()
                workout['has_cash_out'] = 'cash-out' in description_text.lower()
                workout['is_complex'] = self._detect_complex_workout(description_text)
                
                workout['description_lines'] = self._parse_description_lines(description_container)
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
            
            tags_el = card.select_one('[class*="wod-terms"], [class*="tag"]')
            if tags_el:
                tags = [tag.get_text().strip() for tag in tags_el.find_all('a, span')]
                workout['tags'] = [t for t in tags if t and len(t) < 50]
            else:
                workout['tags'] = ['hyrox']
            
            bg_image_el = card.select_one('[class*="namesake-wod-preview"][style*="background-image"]')
            if bg_image_el:
                style = bg_image_el.get('style', '')
                url_match = re.search(r"url\(['\"]?([^'\"]+)['\"]?\)", style)
                workout['background_image'] = url_match.group(1) if url_match else None
            else:
                workout['background_image'] = None
            
            stats_el = card.select_one('[data-id]')
            if stats_el:
                workout['stats'] = self._parse_stats(stats_el)
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
    
    def _extract_workout_type(self, text: str) -> str:
        """
        Extract workout type from description text
        
        Args:
            text: Description text
            
        Returns:
            Workout type enum value
        """
        text_lower = text.lower()
        
        for key, value in self.WORKOUT_TYPES.items():
            if key in text_lower:
                return value
        
        return 'unknown'
    
    def _extract_workout_goal(self, text: str) -> str:
        """
        Extract workout goal from description text
        
        Args:
            text: Description text
            
        Returns:
            Workout goal enum value
        """
        text_lower = text.lower()
        
        for key, value in self.WORKOUT_GOALS.items():
            if key in text_lower:
                return value
        
        return 'unknown'
    
    def _extract_time_specification(self, text: str) -> Optional[str]:
        """
        Extract time specification (e.g., "25 minutes", "40 seconds")
        
        Args:
            text: Description text
            
        Returns:
            Time specification string or None
        """
        time_patterns = [
            r'(\d+)\s*minutes?',
            r'(\d+)\s*seconds?',
            r'(\d+)\s*hours?'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        return None
    
    def _extract_total_minutes(self, text: str) -> Optional[int]:
        """
        Extract total workout time in minutes
        
        Args:
            text: Description text
            
        Returns:
            Total minutes or None
        """
        time_match = re.search(r'amrap\s+in\s+(\d+)\s*minutes?', text, re.IGNORECASE)
        if time_match:
            return int(time_match.group(1))
        
        time_match = re.search(r'emom\s+(\d+)\s*minutes?', text, re.IGNORECASE)
        if time_match:
            return int(time_match.group(1))
        
        time_match = re.search(r'time\s*cap[:\s]+(\d+)\s*minutes?', text, re.IGNORECASE)
        if time_match:
            return int(time_match.group(1))
        
        return None
    
    def _extract_time_cap(self, text: str) -> Optional[int]:
        """
        Extract time cap in minutes
        
        Args:
            text: Description text
            
        Returns:
            Time cap minutes or None
        """
        time_match = re.search(r'time\s*cap[:\s]+(\d+)\s*minutes?', text, re.IGNORECASE)
        if time_match:
            return int(time_match.group(1))
        
        return None
    
    def _detect_complex_workout(self, text: str) -> bool:
        """
        Detect if workout is complex (has mini circuits, ladders, etc.)
        
        Args:
            text: Description text
            
        Returns:
            True if complex workout
        """
        indicators = [
            'mini circuit', 'circuit 1', 'circuit 2', 'round 1:', 'round 2:',
            'ladder', 'rung', 'minutes 0-8', 'minutes 8-10', 'explicit'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in indicators)
    
    def _parse_description_lines(self, container) -> List[Dict]:
        """
        Parse description lines into structured data
        
        Args:
            container: BeautifulSoup element containing description
            
        Returns:
            List of line dictionaries
        """
        lines = []
        spans = container.find_all('span')
        
        for i, span in enumerate(spans):
            text = span.get_text().strip()
            if not text:
                continue
            
            line_data = {
                'line_number': i + 1,
                'line_text': text,
                'is_rest': text.lower().startswith('rest') or 'rest' in text.lower(),
                'is_buy_in': text.lower().startswith('buy-in'),
                'is_cash_out': text.lower().startswith('cash-out'),
            }
            
            line_data.update(self._parse_movement_line(text))
            
            lines.append(line_data)
        
        return lines
    
    def _parse_movement_line(self, text: str) -> Dict:
        """
        Parse a single movement line to extract metrics
        
        Args:
            text: Movement line text
            
        Returns:
            Dictionary with parsed movement data
        """
        movement_data = {
            'movement_name': None,
            'metric_type': None,
            'reps': None,
            'distance_meters': None,
            'duration_seconds': None,
            'calories': None,
            'weight_text': None,
            'is_max_effort': False
        }
        
        text_lower = text.lower()
        
        if 'max' in text_lower:
            movement_data['is_max_effort'] = True
            movement_data['metric_type'] = 'time'
        
        reps_match = re.search(r'(\d+)\s*(?:reps|repetitions)', text, re.IGNORECASE)
        if reps_match:
            movement_data['reps'] = int(reps_match.group(1))
            if not movement_data['metric_type']:
                movement_data['metric_type'] = 'reps'
        
        distance_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:meter|m|m)', text, re.IGNORECASE)
        if distance_match:
            movement_data['distance_meters'] = float(distance_match.group(1))
            if not movement_data['metric_type']:
                movement_data['metric_type'] = 'distance'
        
        duration_match = re.search(r'(\d+)\s*(?:second|sec|minute|min)s?', text, re.IGNORECASE)
        if duration_match:
            duration = int(duration_match.group(1))
            if 'minute' in text_lower or 'min' in text_lower:
                movement_data['duration_seconds'] = duration * 60
            else:
                movement_data['duration_seconds'] = duration
            if not movement_data['metric_type']:
                movement_data['metric_type'] = 'time'
        
        calories_match = re.search(r'(\d+)\s*calorie', text, re.IGNORECASE)
        if calories_match:
            movement_data['calories'] = int(calories_match.group(1))
            if not movement_data['metric_type']:
                movement_data['metric_type'] = 'calories'
        
        weight_match = re.search(r'\((\d+(?:/\d+)?)\s*(?:lb|lbs?|kg|kgs?)\)', text)
        if weight_match:
            movement_data['weight_text'] = weight_match.group(1)
        
        if not movement_data['metric_type']:
            movement_data['metric_type'] = 'reps'
        
        clean_text = re.sub(r'\([^)]*\)', '', text)
        clean_text = re.sub(r'\d+\s*(?:second|sec|minute|min|meter|m|calorie)s?\s*(?:for|max)?', '', clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'\((\d+(?:/\d+)?)\s*(?:lb|lbs?|kg|kgs?)\)', '', clean_text)
        clean_text = clean_text.strip()
        
        movement_data['movement_name'] = clean_text if clean_text else text
        
        return movement_data
    
    def _parse_stats(self, stats_el) -> Dict:
        """
        Parse favorite and comment counts from stats element
        
        Args:
            stats_el: BeautifulSoup element
            
        Returns:
            Dictionary with favorites and comments counts
        """
        stats = {'favorites': 0, 'comments': 0}
        
        try:
            favorites_btn = stats_el.find('button', class_=lambda x: x and 'favorite' in str(x))
            if favorites_btn:
                fav_text = favorites_btn.get_text().strip()
                fav_match = re.search(r'(\d+)', fav_text)
                if fav_match:
                    stats['favorites'] = int(fav_match.group(1))
        except:
            pass
        
        try:
            comments_btn = stats_el.find('button', class_=lambda x: x and 'comment' in str(x))
            if comments_btn:
                com_text = comments_btn.get_text().strip()
                com_match = re.search(r'(\d+)', com_text)
                if com_match:
                    stats['comments'] = int(com_match.group(1))
        except:
            pass
        
        return stats
    
    def get_scrape_summary(self) -> Dict:
        """
        Get summary of scraping session
        
        Returns:
            Dictionary with scraping statistics
        """
        return {
            'session_id': self.session_id,
            'total_workouts_found': self.workouts_scraped,
            'workouts_saved': self.workouts_scraped,
            'errors_count': self.errors_count,
            'has_errors': self.errors_count > 0,
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
        workouts = await scraper.scrape_all_workouts(max_workouts=50)
        
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
    asyncio.run(main())
