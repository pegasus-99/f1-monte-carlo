import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple
import random
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class Driver2025:
    name: str
    team: str
    base_speed: float  # Base performance rating (0-100)
    consistency: float  # Consistency factor (0-1, higher = more consistent)
    qualifying_pace: float  # Qualifying performance (0-100)
    race_pace: float  # Race pace performance (0-100)
    reliability: float  # Reliability factor (0-1, higher = more reliable)
    experience: int  # Years in F1
    current_form: float  # Current form multiplier (0.5-1.5)
    # 2025 specific data
    championship_position: int  # Current championship position
    points: int  # Current championship points
    recent_performance: List[int]  # Last 10 race results
    car_news_factor: float  # New: car design news impact (0.9-1.1, 1.0 neutral)
    engine_news_factor: float  # New: engine news impact (0.9-1.1, 1.0 neutral)

class F1MonteCarloSimulation2025:
    def __init__(self):
        self.drivers = self._initialize_2025_drivers()
        self.tracks = self._initialize_2025_tracks()
        self.simulation_results = []
        
    def _initialize_2025_drivers(self) -> Dict[str, Driver2025]:
        """Initialize 2025 F1 drivers with current performance data"""
        # Data based on actual 2025 season performance so far
        drivers_data = {
            "Max Verstappen": Driver2025(
                "Max Verstappen", "Red Bull Racing", 98, 0.95, 98, 99, 0.97, 11, 1.4,
                1, 314, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                0.97, 0.95  # car_news_factor, engine_news_factor (Red Bull: reliability concerns)
            ),
            "Lando Norris": Driver2025(
                "Lando Norris", "McLaren", 92, 0.88, 93, 92, 0.92, 7, 1.4,
                2, 171, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                1.08, 1.05  # McLaren: dominant car, strong engine
            ),
            "Oscar Piastri": Driver2025(
                "Oscar Piastri", "McLaren", 88, 0.84, 89, 88, 0.88, 3, 1.3,
                3, 124, [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                1.08, 1.05
            ),
            "Charles Leclerc": Driver2025(
                "Charles Leclerc", "Ferrari", 89, 0.85, 92, 88, 0.88, 8, 1.2,
                4, 150, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                1.04, 1.03  # Ferrari: new suspension, improved engine
            ),
            "Lewis Hamilton": Driver2025(
                "Lewis Hamilton", "Ferrari", 88, 0.90, 89, 87, 0.89, 18, 0.9,
                5, 110, [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                1.04, 1.03
            ),
            "George Russell": Driver2025(
                "George Russell", "Mercedes", 85, 0.86, 86, 85, 0.87, 6, 1.0,
                6, 111, [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                1.01, 1.02  # Mercedes: W16 evolution, solid engine
            ),
            "Kimi Antonelli": Driver2025(
                "Kimi Antonelli", "Mercedes", 80, 0.80, 81, 80, 0.82, 1, 1.1,
                7, 50, [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                1.01, 1.02
            ),
            "Alexander Albon": Driver2025(
                "Alexander Albon", "Williams", 82, 0.84, 83, 82, 0.85, 6, 1.0,
                8, 38, [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                0.96, 0.97  # Williams: car/engine still behind
            ),
            "Carlos Sainz": Driver2025(
                "Carlos Sainz", "Williams", 87, 0.89, 88, 87, 0.90, 10, 1.1,
                9, 135, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                0.96, 0.97
            ),
            "Nico Hulkenberg": Driver2025(
                "Nico Hulkenberg", "Kick Sauber", 81, 0.83, 82, 81, 0.83, 14, 1.0,
                10, 44, [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                0.95, 0.96  # Kick Sauber: limited
            ),
            "Gabriel Bortoleto": Driver2025(
                "Gabriel Bortoleto", "Kick Sauber", 78, 0.77, 79, 78, 0.81, 1, 1.2,
                11, 20, [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
                0.95, 0.96
            ),
            "Liam Lawson": Driver2025(
                "Liam Lawson", "Racing Bulls", 82, 0.83, 83, 82, 0.84, 2, 1.1,
                12, 30, [12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
                1.00, 0.98  # Racing Bulls: solid but not top
            ),
            "Isack Hadjar": Driver2025(
                "Isack Hadjar", "Racing Bulls", 79, 0.78, 80, 79, 0.80, 1, 1.0,
                13, 25, [13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
                1.00, 0.98
            ),
            "Lance Stroll": Driver2025(
                "Lance Stroll", "Aston Martin", 82, 0.80, 81, 82, 0.85, 8, 0.9,
                14, 52, [14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
                0.98, 1.00  # Aston: stable but not top tier
            ),
            "Fernando Alonso": Driver2025(
                "Fernando Alonso", "Aston Martin", 75, 0.75, 76, 75, 0.78, 24, 0.7,
                15, 87, [15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
                0.98, 1.00
            ),
            "Esteban Ocon": Driver2025(
                "Esteban Ocon", "Haas", 81, 0.82, 82, 81, 0.84, 8, 0.9,
                16, 28, [16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
                0.95, 0.97  # Haas: limited car/engine
            ),
            "Oliver Bearman": Driver2025(
                "Oliver Bearman", "Haas", 78, 0.77, 79, 78, 0.81, 1, 1.2,
                17, 15, [17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
                0.95, 0.97
            ),
            "Pierre Gasly": Driver2025(
                "Pierre Gasly", "Alpine", 82, 0.83, 83, 82, 0.85, 8, 0.9,
                18, 26, [18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
                0.94, 0.95  # Alpine: struggling
            ),
            "Franco Colapinto": Driver2025(
                "Franco Colapinto", "Alpine", 77, 0.76, 78, 77, 0.80, 1, 1.1,
                19, 10, [19, 19, 19, 19, 19, 19, 19, 19, 19, 19],
                0.94, 0.95
            ),
            "Yuki Tsunoda": Driver2025(
                "Yuki Tsunoda", "Red Bull Racing", 83, 0.82, 84, 83, 0.84, 5, 1.1,
                20, 200, [20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
                0.97, 0.95
            )
        }
        return drivers_data
    
    def _initialize_2025_tracks(self) -> Dict[str, Dict]:
        """Initialize 2025 F1 tracks with current characteristics"""
        tracks = {
            "Bahrain": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.6,
                "tire_wear": 0.8,
                "season_round": 1
            },
            "Saudi Arabia": {
                "type": "street_circuit",
                "overtaking_difficulty": 0.3,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.5,
                "tire_wear": 0.7,
                "season_round": 2
            },
            "Australia": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.5,
                "technical_demand": 0.6,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.6,
                "season_round": 3
            },
            "Japan": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.6,
                "technical_demand": 0.9,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.7,
                "season_round": 4
            },
            "China": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.7,
                "tire_wear": 0.8,
                "season_round": 5
            },
            "Miami": {
                "type": "street_circuit",
                "overtaking_difficulty": 0.5,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.6,
                "tire_wear": 0.7,
                "season_round": 6
            },
            "Emilia Romagna": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.7,
                "season_round": 7
            },
            "Monaco": {
                "type": "street_circuit",
                "overtaking_difficulty": 0.9,
                "technical_demand": 0.95,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.7,
                "season_round": 8
            },
            "Canada": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.3,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.9,
                "tire_wear": 0.6,
                "season_round": 9
            },
            "Spain": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.7,
                "tire_wear": 0.7,
                "season_round": 10
            },
            "Austria": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.2,
                "technical_demand": 0.6,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.5,
                "season_round": 11
            },
            "Great Britain": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.3,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.9,
                "tire_wear": 0.6,
                "season_round": 12
            },
            "Hungary": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.7,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.7,
                "tire_wear": 0.8,
                "season_round": 13
            },
            "Belgium": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.9,
                "weather_sensitivity": 0.95,
                "tire_wear": 0.5,
                "season_round": 14
            },
            "Netherlands": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.3,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.6,
                "season_round": 15
            },
            "Italy": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.2,
                "technical_demand": 0.6,
                "weather_sensitivity": 0.7,
                "tire_wear": 0.8,
                "season_round": 16
            },
            "Azerbaijan": {
                "type": "street_circuit",
                "overtaking_difficulty": 0.3,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.6,
                "tire_wear": 0.7,
                "season_round": 17
            },
            "Singapore": {
                "type": "street_circuit",
                "overtaking_difficulty": 0.8,
                "technical_demand": 0.9,
                "weather_sensitivity": 0.7,
                "tire_wear": 0.8,
                "season_round": 18
            },
            "United States": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.6,
                "season_round": 19
            },
            "Mexico": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.5,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.6,
                "tire_wear": 0.7,
                "season_round": 20
            },
            "Brazil": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.3,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.8,
                "tire_wear": 0.6,
                "season_round": 21
            },
            "Las Vegas": {
                "type": "street_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.5,
                "tire_wear": 0.7,
                "season_round": 22
            },
            "Qatar": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.5,
                "technical_demand": 0.8,
                "weather_sensitivity": 0.6,
                "tire_wear": 0.8,
                "season_round": 23
            },
            "Abu Dhabi": {
                "type": "permanent_circuit",
                "overtaking_difficulty": 0.4,
                "technical_demand": 0.7,
                "weather_sensitivity": 0.5,
                "tire_wear": 0.6,
                "season_round": 24
            }
        }
        return tracks
    
    def simulate_qualifying(self, track_name: str, num_simulations: int = 1000) -> List[Tuple[str, float]]:
        """Simulate qualifying session with 2025 data and car/engine news factors"""
        track = self.tracks.get(track_name, self.tracks["Bahrain"])
        qualifying_results = []
        for _ in range(num_simulations):
            driver_times = []
            for driver_name, driver in self.drivers.items():
                base_time = 80 - driver.qualifying_pace * 0.6
                consistency_factor = np.random.normal(0, (1 - driver.consistency) * 3)
                if track["type"] == "street_circuit":
                    experience_bonus = driver.experience * 0.05
                else:
                    experience_bonus = 0
                form_adjustment = (driver.current_form - 1.0) * 1
                track_randomness = np.random.normal(0, 2)
                recent_avg = np.mean(driver.recent_performance) if driver.recent_performance else 10
                # Use last 10 finishes for recent form bonus
                recent_form_bonus = (recent_avg - 10) * 0.2  # Lower avg = better performance = bonus
                # Integrate car/engine news factors (lower time = better)
                car_engine_bonus = (2.0 - (driver.car_news_factor + driver.engine_news_factor)) * 2.0  # up to +/-0.4s
                final_time = base_time + consistency_factor + form_adjustment - experience_bonus + track_randomness - recent_form_bonus - car_engine_bonus
                driver_times.append((driver_name, final_time))
            driver_times.sort(key=lambda x: x[1])
            qualifying_results.append(driver_times)
        return qualifying_results
    
    def simulate_race(self, track_name: str, qualifying_results: List[Tuple[str, float]], 
                     num_simulations: int = 1000) -> List[List[str]]:
        """Simulate race based on qualifying results with 2025 data and car/engine news factors"""
        track = self.tracks.get(track_name, self.tracks["Bahrain"])
        race_results = []
        for sim in range(num_simulations):
            starting_grid = [driver for driver, _ in qualifying_results[sim]]
            final_positions = starting_grid.copy()
            for lap in range(50):
                for i, driver_name in enumerate(final_positions):
                    if driver_name in self.drivers:
                        driver = self.drivers[driver_name]
                        dnf_prob = (1 - driver.reliability) * 0.001
                        if np.random.random() < dnf_prob:
                            final_positions.remove(driver_name)
                            final_positions.append(driver_name)
                for i in range(len(final_positions) - 1):
                    if i >= len(final_positions) - 1:
                        break
                    driver_ahead = self.drivers.get(final_positions[i])
                    driver_behind = self.drivers.get(final_positions[i + 1])
                    if driver_ahead and driver_behind:
                        pace_diff = driver_behind.race_pace - driver_ahead.race_pace
                        # Integrate car/engine news factors into overtake probability
                        car_engine_factor = ((driver_behind.car_news_factor + driver_behind.engine_news_factor) - (driver_ahead.car_news_factor + driver_ahead.engine_news_factor)) * 0.5
                        overtake_prob = max(0, pace_diff * 0.01 * (1 - track["overtaking_difficulty"]))
                        recent_form_diff = (np.mean(driver_behind.recent_performance) - np.mean(driver_ahead.recent_performance)) * 0.02
                        overtake_prob += recent_form_diff + car_engine_factor
                        if np.random.random() < overtake_prob:
                            final_positions[i], final_positions[i + 1] = final_positions[i + 1], final_positions[i]
            race_results.append(final_positions)
        return race_results
    
    def run_monte_carlo_simulation(self, track_name: str, num_simulations: int = 10000) -> Dict:
        """Run complete Monte Carlo simulation for a race"""
        print(f"Running Monte Carlo simulation for {track_name}...")
        print(f"Number of simulations: {num_simulations}")
        
        # Simulate qualifying
        qualifying_results = self.simulate_qualifying(track_name, num_simulations)
        
        # Simulate race
        race_results = self.simulate_race(track_name, qualifying_results, num_simulations)
        
        # Analyze results
        win_probabilities = self._calculate_win_probabilities(race_results)
        podium_probabilities = self._calculate_podium_probabilities(race_results)
        points_probabilities = self._calculate_points_probabilities(race_results)
        
        results = {
            "track": track_name,
            "num_simulations": num_simulations,
            "timestamp": datetime.now().isoformat(),
            "win_probabilities": win_probabilities,
            "podium_probabilities": podium_probabilities,
            "points_probabilities": points_probabilities,
            "race_results": race_results[:100]  # Store first 100 results for analysis
        }
        
        self.simulation_results.append(results)
        return results
    
    def _calculate_win_probabilities(self, race_results: List[List[str]]) -> Dict[str, float]:
        """Calculate probability of each driver winning"""
        win_counts = {}
        total_races = len(race_results)
        
        for driver_name in self.drivers.keys():
            win_counts[driver_name] = 0
        
        for race in race_results:
            if race:  # Check if race has results
                winner = race[0]
                if winner in win_counts:
                    win_counts[winner] += 1
        
        win_probabilities = {driver: count / total_races for driver, count in win_counts.items()}
        return win_probabilities
    
    def _calculate_podium_probabilities(self, race_results: List[List[str]]) -> Dict[str, float]:
        """Calculate probability of each driver finishing on the podium"""
        podium_counts = {}
        total_races = len(race_results)
        
        for driver_name in self.drivers.keys():
            podium_counts[driver_name] = 0
        
        for race in race_results:
            for i, driver in enumerate(race[:3]):  # Top 3 positions
                if driver in podium_counts:
                    podium_counts[driver] += 1
        
        podium_probabilities = {driver: count / total_races for driver, count in podium_counts.items()}
        return podium_probabilities
    
    def _calculate_points_probabilities(self, race_results: List[List[str]]) -> Dict[str, float]:
        """Calculate probability of each driver scoring points (top 10)"""
        points_counts = {}
        total_races = len(race_results)
        
        for driver_name in self.drivers.keys():
            points_counts[driver_name] = 0
        
        for race in race_results:
            for i, driver in enumerate(race[:10]):  # Top 10 positions
                if driver in points_counts:
                    points_counts[driver] += 1
        
        points_probabilities = {driver: count / total_races for driver, count in points_counts.items()}
        return points_probabilities
    
    def get_prediction_summary(self, results: Dict) -> str:
        """Generate a text summary of the simulation results"""
        win_probs = results["win_probabilities"]
        podium_probs = results["podium_probabilities"]
        
        # Top 5 most likely winners
        sorted_winners = sorted(win_probs.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = f"F1 2025 Race Prediction - {results['track']}\n"
        summary += f"Based on {results['num_simulations']:,} Monte Carlo simulations\n\n"
        summary += "Top 5 Most Likely Winners:\n"
        
        for i, (driver, prob) in enumerate(sorted_winners, 1):
            podium_prob = podium_probs[driver]
            team = self.drivers[driver].team
            championship_pos = self.drivers[driver].championship_position
            points = self.drivers[driver].points
            summary += f"{i}. {driver} ({team}): {prob:.1%} win, {podium_prob:.1%} podium\n"
            summary += f"   Championship: #{championship_pos} ({points} pts)\n"
        
        return summary

# Example usage
if __name__ == "__main__":
    # Create simulation instance
    f1_sim_2025 = F1MonteCarloSimulation2025()
    
    # Run simulation for upcoming races
    upcoming_races = ["Monaco", "Canada", "Spain", "Austria", "Great Britain"]
    
    for track in upcoming_races:
        print(f"\n{'='*50}")
        results = f1_sim_2025.run_monte_carlo_simulation(track, num_simulations=5000)
        
        # Print summary
        summary = f1_sim_2025.get_prediction_summary(results)
        print(summary) 