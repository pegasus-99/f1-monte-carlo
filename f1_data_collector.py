import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class F1DataCollector:
    """Collect F1 historical data from the last 3 years"""
    
    def __init__(self):
        self.base_url = "http://ergast.com/api/f1"
        self.data = {}
        
    def get_season_data(self, year: int) -> Dict:
        """Get complete season data for a specific year"""
        print(f"Collecting data for {year} season...")
        
        season_data = {
            'races': [],
            'qualifying': [],
            'results': [],
            'drivers': [],
            'constructors': []
        }
        
        # Get races
        races_url = f"{self.base_url}/{year}/races.json"
        try:
            response = requests.get(races_url)
            if response.status_code == 200:
                races_data = response.json()
                season_data['races'] = races_data['MRData']['RaceTable']['Races']
                print(f"  - Found {len(season_data['races'])} races")
        except Exception as e:
            print(f"  - Error getting races: {e}")
        
        # Get qualifying results for each race
        for race in season_data['races']:
            round_num = race['round']
            qualifying_url = f"{self.base_url}/{year}/{round_num}/qualifying.json"
            try:
                response = requests.get(qualifying_url)
                if response.status_code == 200:
                    quali_data = response.json()
                    if 'QualifyingResults' in quali_data['MRData']['RaceTable']['Races'][0]:
                        quali_results = quali_data['MRData']['RaceTable']['Races'][0]['QualifyingResults']
                        for result in quali_results:
                            result['race_round'] = round_num
                            result['race_name'] = race['raceName']
                            result['circuit'] = race['Circuit']['circuitName']
                        season_data['qualifying'].extend(quali_results)
                time.sleep(0.1)  # Be nice to the API
            except Exception as e:
                print(f"  - Error getting qualifying for round {round_num}: {e}")
        
        # Get race results for each race
        for race in season_data['races']:
            round_num = race['round']
            results_url = f"{self.base_url}/{year}/{round_num}/results.json"
            try:
                response = requests.get(results_url)
                if response.status_code == 200:
                    results_data = response.json()
                    if 'Results' in results_data['MRData']['RaceTable']['Races'][0]:
                        race_results = results_data['MRData']['RaceTable']['Races'][0]['Results']
                        for result in race_results:
                            result['race_round'] = round_num
                            result['race_name'] = race['raceName']
                            result['circuit'] = race['Circuit']['circuitName']
                        season_data['results'].extend(race_results)
                time.sleep(0.1)  # Be nice to the API
            except Exception as e:
                print(f"  - Error getting results for round {round_num}: {e}")
        
        # Get drivers
        drivers_url = f"{self.base_url}/{year}/drivers.json"
        try:
            response = requests.get(drivers_url)
            if response.status_code == 200:
                drivers_data = response.json()
                season_data['drivers'] = drivers_data['MRData']['DriverTable']['Drivers']
        except Exception as e:
            print(f"  - Error getting drivers: {e}")
        
        # Get constructors
        constructors_url = f"{self.base_url}/{year}/constructors.json"
        try:
            response = requests.get(constructors_url)
            if response.status_code == 200:
                constructors_data = response.json()
                season_data['constructors'] = constructors_data['MRData']['ConstructorTable']['Constructors']
        except Exception as e:
            print(f"  - Error getting constructors: {e}")
        
        return season_data
    
    def collect_three_years_data(self) -> Dict:
        """Collect data for the last 3 years"""
        current_year = datetime.now().year
        years = [current_year - 2, current_year - 1, current_year]
        
        all_data = {}
        for year in years:
            all_data[year] = self.get_season_data(year)
            time.sleep(1)  # Be nice to the API
        
        return all_data
    
    def calculate_driver_ratings(self, data: Dict) -> Dict:
        """Calculate driver ratings based on historical performance"""
        driver_stats = {}
        
        for year, year_data in data.items():
            for result in year_data['results']:
                driver_id = result['Driver']['driverId']
                driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
                
                if driver_id not in driver_stats:
                    driver_stats[driver_id] = {
                        'name': driver_name,
                        'results': [],
                        'qualifying': [],
                        'dnfs': 0,
                        'total_races': 0,
                        'wins': 0,
                        'podiums': 0,
                        'points_finishes': 0
                    }
                
                # Race results
                position = result.get('position', 'DNF')
                if position == 'DNF':
                    driver_stats[driver_id]['dnfs'] += 1
                else:
                    position = int(position)
                    driver_stats[driver_id]['results'].append(position)
                    
                    if position == 1:
                        driver_stats[driver_id]['wins'] += 1
                    if position <= 3:
                        driver_stats[driver_id]['podiums'] += 1
                    if position <= 10:
                        driver_stats[driver_id]['points_finishes'] += 1
                
                driver_stats[driver_id]['total_races'] += 1
        
        # Calculate qualifying performance
        for year, year_data in data.items():
            for quali in year_data['qualifying']:
                driver_id = quali['Driver']['driverId']
                if driver_id in driver_stats:
                    position = int(quali.get('position', 20))
                    driver_stats[driver_id]['qualifying'].append(position)
        
        # Calculate ratings
        driver_ratings = {}
        for driver_id, stats in driver_stats.items():
            if stats['total_races'] < 5:  # Skip drivers with too few races
                continue
                
            # Calculate average finishing position
            avg_finish = np.mean(stats['results']) if stats['results'] else 20
            
            # Calculate qualifying performance
            avg_quali = np.mean(stats['qualifying']) if stats['qualifying'] else 20
            
            # Calculate reliability
            reliability = 1 - (stats['dnfs'] / stats['total_races'])
            
            # Calculate consistency (standard deviation of results)
            consistency = 1 - (np.std(stats['results']) / 20) if len(stats['results']) > 1 else 0.5
            
            # Calculate win rate and podium rate
            win_rate = stats['wins'] / stats['total_races']
            podium_rate = stats['podiums'] / stats['total_races']
            
            # Convert to 0-100 scale
            base_speed = max(0, 100 - avg_finish * 3)  # Better position = higher rating
            qualifying_pace = max(0, 100 - avg_quali * 3)
            race_pace = base_speed * 0.8 + win_rate * 20 + podium_rate * 10
            
            driver_ratings[driver_id] = {
                'name': stats['name'],
                'base_speed': round(base_speed, 1),
                'qualifying_pace': round(qualifying_pace, 1),
                'race_pace': round(race_pace, 1),
                'consistency': round(consistency, 2),
                'reliability': round(reliability, 2),
                'total_races': stats['total_races'],
                'wins': stats['wins'],
                'podiums': stats['podiums'],
                'avg_finish': round(avg_finish, 1),
                'avg_quali': round(avg_quali, 1)
            }
        
        return driver_ratings
    
    def calculate_track_characteristics(self, data: Dict) -> Dict:
        """Calculate track characteristics based on historical data"""
        track_stats = {}
        
        for year, year_data in data.items():
            for result in year_data['results']:
                circuit = result['circuit']
                
                if circuit not in track_stats:
                    track_stats[circuit] = {
                        'races': [],
                        'dnf_rate': 0,
                        'overtaking_opportunities': 0,
                        'technical_demand': 0
                    }
                
                # Calculate DNF rate
                total_finishers = len([r for r in year_data['results'] if r['circuit'] == circuit])
                dnfs = len([r for r in year_data['results'] if r['circuit'] == circuit and r.get('position') == 'DNF'])
                track_stats[circuit]['dnf_rate'] = dnfs / total_finishers if total_finishers > 0 else 0
                
                # Store race data for further analysis
                track_stats[circuit]['races'].append({
                    'year': year,
                    'results': [r for r in year_data['results'] if r['circuit'] == circuit]
                })
        
        # Calculate track characteristics
        track_characteristics = {}
        for circuit, stats in track_stats.items():
            if len(stats['races']) < 2:  # Skip tracks with too few races
                continue
            
            # Calculate overtaking difficulty based on position changes
            overtaking_difficulty = min(0.9, max(0.1, stats['dnf_rate'] * 2))
            
            # Estimate technical demand (higher for tracks with more DNFs)
            technical_demand = min(0.95, max(0.3, stats['dnf_rate'] * 3))
            
            track_characteristics[circuit] = {
                'type': 'permanent_circuit',  # Default, can be updated manually
                'overtaking_difficulty': round(overtaking_difficulty, 2),
                'technical_demand': round(technical_demand, 2),
                'weather_sensitivity': 0.7,  # Default
                'tire_wear': 0.6,  # Default
                'dnf_rate': round(stats['dnf_rate'], 3),
                'races_analyzed': len(stats['races'])
            }
        
        return track_characteristics
    
    def save_data(self, data: Dict, filename: str = "f1_historical_data.json"):
        """Save collected data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Data saved to {filename}")
    
    def load_data(self, filename: str = "f1_historical_data.json") -> Dict:
        """Load data from JSON file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found. Run data collection first.")
            return {}

def main():
    """Main function to collect and analyze F1 data"""
    collector = F1DataCollector()
    
    print("🏎️ F1 Historical Data Collector")
    print("=" * 50)
    
    # Collect data for last 3 years
    data = collector.collect_three_years_data()
    
    # Calculate driver ratings
    print("\n📊 Calculating driver ratings...")
    driver_ratings = collector.calculate_driver_ratings(data)
    
    # Calculate track characteristics
    print("🏁 Calculating track characteristics...")
    track_characteristics = collector.calculate_track_characteristics(data)
    
    # Save everything
    output_data = {
        'raw_data': data,
        'driver_ratings': driver_ratings,
        'track_characteristics': track_characteristics,
        'analysis_date': datetime.now().isoformat()
    }
    
    collector.save_data(output_data)
    
    # Print summary
    print(f"\n✅ Data collection complete!")
    print(f"📈 Analyzed {len(driver_ratings)} drivers")
    print(f"🏁 Analyzed {len(track_characteristics)} tracks")
    
    # Show top 5 drivers
    print("\n🏆 Top 5 Drivers by Rating:")
    sorted_drivers = sorted(driver_ratings.items(), key=lambda x: x[1]['base_speed'], reverse=True)[:5]
    for i, (driver_id, stats) in enumerate(sorted_drivers, 1):
        print(f"{i}. {stats['name']}: {stats['base_speed']} rating, {stats['wins']} wins, {stats['podiums']} podiums")

if __name__ == "__main__":
    main() 