import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import random
from datetime import datetime

class TireCompound(Enum):
    SOFT = "soft"
    MEDIUM = "medium"
    HARD = "hard"
    INTERMEDIATE = "intermediate"
    WET = "wet"

class WeatherCondition(Enum):
    DRY = "dry"
    LIGHT_RAIN = "light_rain"
    HEAVY_RAIN = "heavy_rain"
    DRIZZLE = "drizzle"

@dataclass
class Driver:
    name: str
    team: str
    # Core driver attributes (0-100 scale)
    raw_pace: float  # Natural speed
    consistency: float  # How consistent they are (0-1)
    tire_management: float  # How well they manage tires
    race_craft: float  # Overtaking/defending ability
    mental_strength: float  # Pressure handling
    physical_fitness: float  # Endurance
    experience: int  # Years in F1
    
    # Current form and recent performance
    current_form: float  # Multiplier (0.5-1.5)
    recent_results: List[int]  # Last 10 race positions
    
    # Championship data
    championship_position: int
    championship_points: int

@dataclass
class Car:
    team: str
    # Car performance attributes (0-100 scale)
    aero_efficiency: float
    engine_power: float
    reliability: float  # 0-1, higher = more reliable
    tire_degradation: float  # How quickly tires wear
    fuel_efficiency: float
    straight_line_speed: float
    cornering_speed: float
    
    # Development status
    car_upgrade_factor: float  # 0.9-1.1, 1.0 = neutral

@dataclass
class Track:
    name: str
    # Track characteristics
    base_qualifying_time: float  # Base lap time in seconds
    overtaking_difficulty: float  # 0-1, higher = harder to overtake
    tire_wear_rate: float  # 0-1, higher = more tire wear
    fuel_consumption: float  # 0-1, higher = more fuel consumption
    weather_sensitivity: float  # 0-1, how much weather affects performance
    technical_demand: float  # 0-1, how technically demanding
    track_type: str  # "permanent", "street", "hybrid"
    
    # Weather conditions
    weather: WeatherCondition = WeatherCondition.DRY
    temperature: float = 25.0  # Celsius
    humidity: float = 50.0  # Percentage

@dataclass
class TireStrategy:
    compound: TireCompound
    age: int  # Laps used
    wear: float  # 0-1, 1 = completely worn
    temperature: float  # Tire temperature

class F1RealisticSimulation:
    def __init__(self):
        self.drivers = self._initialize_drivers()
        self.cars = self._initialize_cars()
        self.tracks = self._initialize_tracks()
        self.results = []
        
    def _initialize_drivers(self) -> Dict[str, Driver]:
        """Initialize realistic driver data based on 2024/2025 performance"""
        return {
            "Max Verstappen": Driver(
                "Max Verstappen", "Red Bull Racing",
                98, 0.95, 95, 95, 98, 95, 11,  # Core attributes
                1.4, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Form and recent results
                1, 314  # Championship
            ),
            "Lando Norris": Driver(
                "Lando Norris", "McLaren",
                92, 0.88, 88, 90, 85, 90, 7,
                1.3, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                2, 171
            ),
            "Oscar Piastri": Driver(
                "Oscar Piastri", "McLaren",
                88, 0.85, 85, 87, 80, 88, 3,
                1.2, [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                3, 124
            ),
            "Charles Leclerc": Driver(
                "Charles Leclerc", "Ferrari",
                90, 0.82, 92, 88, 85, 88, 8,
                1.1, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                4, 150
            ),
            "Lewis Hamilton": Driver(
                "Lewis Hamilton", "Ferrari",
                88, 0.90, 89, 87, 90, 92, 18,
                0.9, [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                5, 110
            ),
            "George Russell": Driver(
                "George Russell", "Mercedes",
                85, 0.86, 86, 85, 82, 85, 6,
                1.0, [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                6, 111
            ),
            "Kimi Antonelli": Driver(
                "Kimi Antonelli", "Mercedes",
                80, 0.75, 78, 80, 75, 80, 1,
                1.1, [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                7, 50
            ),
            "Alexander Albon": Driver(
                "Alexander Albon", "Williams",
                82, 0.84, 83, 82, 78, 82, 6,
                1.0, [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                8, 38
            ),
            "Carlos Sainz": Driver(
                "Carlos Sainz", "Williams",
                87, 0.89, 88, 87, 85, 87, 10,
                1.1, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                9, 135
            ),
            "Nico Hulkenberg": Driver(
                "Nico Hulkenberg", "Kick Sauber",
                81, 0.83, 82, 81, 80, 81, 14,
                1.0, [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                10, 44
            ),
            "Gabriel Bortoleto": Driver(
                "Gabriel Bortoleto", "Kick Sauber",
                78, 0.70, 76, 78, 72, 78, 1,
                1.2, [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
                11, 20
            ),
            "Liam Lawson": Driver(
                "Liam Lawson", "Racing Bulls",
                82, 0.83, 83, 82, 78, 82, 2,
                1.1, [12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
                12, 30
            ),
            "Isack Hadjar": Driver(
                "Isack Hadjar", "Racing Bulls",
                79, 0.75, 78, 79, 75, 79, 1,
                1.0, [13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
                13, 25
            ),
            "Lance Stroll": Driver(
                "Lance Stroll", "Aston Martin",
                82, 0.80, 81, 82, 78, 82, 8,
                0.9, [14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
                14, 52
            ),
            "Fernando Alonso": Driver(
                "Fernando Alonso", "Aston Martin",
                85, 0.85, 86, 85, 90, 88, 24,
                0.8, [15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
                15, 87
            ),
            "Esteban Ocon": Driver(
                "Esteban Ocon", "Haas",
                81, 0.82, 82, 81, 80, 81, 8,
                0.9, [16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
                16, 28
            ),
            "Oliver Bearman": Driver(
                "Oliver Bearman", "Haas",
                78, 0.75, 77, 78, 75, 78, 1,
                1.2, [17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
                17, 15
            ),
            "Pierre Gasly": Driver(
                "Pierre Gasly", "Alpine",
                82, 0.83, 83, 82, 80, 82, 8,
                0.9, [18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
                18, 26
            ),
            "Franco Colapinto": Driver(
                "Franco Colapinto", "Alpine",
                77, 0.70, 76, 77, 72, 77, 1,
                1.1, [19, 19, 19, 19, 19, 19, 19, 19, 19, 19],
                19, 10
            ),
            "Yuki Tsunoda": Driver(
                "Yuki Tsunoda", "Red Bull Racing",
                80, 0.75, 82, 80, 75, 80, 5,
                1.0, [20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
                20, 200
            )
        }
    
    def _initialize_cars(self) -> Dict[str, Car]:
        """Initialize car performance data"""
        return {
            "Red Bull Racing": Car(
                "Red Bull Racing",
                95, 92, 0.95, 0.85, 90, 94, 96,  # Performance attributes
                0.98  # Slight reliability concerns
            ),
            "McLaren": Car(
                "McLaren",
                94, 90, 0.92, 0.80, 88, 92, 94,
                1.05  # Strong development
            ),
            "Ferrari": Car(
                "Ferrari",
                92, 88, 0.88, 0.82, 85, 90, 92,
                1.03  # Good development
            ),
            "Mercedes": Car(
                "Mercedes",
                88, 86, 0.90, 0.85, 87, 88, 90,
                1.01  # Stable
            ),
            "Williams": Car(
                "Williams",
                82, 80, 0.85, 0.90, 80, 82, 84,
                0.96  # Limited development
            ),
            "Kick Sauber": Car(
                "Kick Sauber",
                78, 76, 0.80, 0.92, 75, 78, 80,
                0.95  # Limited resources
            ),
            "Racing Bulls": Car(
                "Racing Bulls",
                84, 82, 0.82, 0.88, 82, 84, 86,
                0.98  # Red Bull B-team
            ),
            "Aston Martin": Car(
                "Aston Martin",
                86, 84, 0.88, 0.86, 84, 86, 88,
                0.98  # Stable
            ),
            "Haas": Car(
                "Haas",
                80, 78, 0.78, 0.94, 76, 80, 82,
                0.95  # Limited development
            ),
            "Alpine": Car(
                "Alpine",
                82, 80, 0.80, 0.90, 78, 82, 84,
                0.94  # Struggling
            )
        }
    
    def _initialize_tracks(self) -> Dict[str, Track]:
        """Initialize track data with realistic characteristics"""
        return {
            "Bahrain": Track(
                "Bahrain", 85.0, 0.4, 0.8, 0.7, 0.6, 0.7, "permanent"
            ),
            "Saudi Arabia": Track(
                "Saudi Arabia", 88.0, 0.3, 0.7, 0.8, 0.5, 0.8, "street"
            ),
            "Australia": Track(
                "Australia", 82.0, 0.5, 0.6, 0.6, 0.8, 0.6, "permanent"
            ),
            "Japan": Track(
                "Japan", 90.0, 0.6, 0.7, 0.8, 0.8, 0.9, "permanent"
            ),
            "China": Track(
                "China", 87.0, 0.4, 0.8, 0.7, 0.7, 0.7, "permanent"
            ),
            "Miami": Track(
                "Miami", 89.0, 0.5, 0.7, 0.8, 0.6, 0.8, "street"
            ),
            "Emilia Romagna": Track(
                "Emilia Romagna", 86.0, 0.4, 0.7, 0.8, 0.8, 0.8, "permanent"
            ),
            "Monaco": Track(
                "Monaco", 92.0, 0.9, 0.7, 0.9, 0.8, 0.95, "street"
            ),
            "Canada": Track(
                "Canada", 84.0, 0.3, 0.6, 0.7, 0.9, 0.7, "permanent"
            ),
            "Spain": Track(
                "Spain", 88.0, 0.4, 0.7, 0.7, 0.7, 0.8, "permanent"
            ),
            "Austria": Track(
                "Austria", 80.0, 0.2, 0.5, 0.6, 0.8, 0.6, "permanent"
            ),
            "Great Britain": Track(
                "Great Britain", 85.0, 0.4, 0.6, 0.7, 0.8, 0.7, "permanent"
            ),
            "Hungary": Track(
                "Hungary", 87.0, 0.7, 0.8, 0.8, 0.7, 0.8, "permanent"
            ),
            "Belgium": Track(
                "Belgium", 89.0, 0.5, 0.6, 0.8, 0.9, 0.8, "permanent"
            ),
            "Netherlands": Track(
                "Netherlands", 86.0, 0.4, 0.7, 0.7, 0.8, 0.7, "permanent"
            ),
            "Italy": Track(
                "Italy", 83.0, 0.3, 0.5, 0.8, 0.7, 0.6, "permanent"
            ),
            "Azerbaijan": Track(
                "Azerbaijan", 91.0, 0.4, 0.6, 0.8, 0.6, 0.8, "street"
            ),
            "Singapore": Track(
                "Singapore", 93.0, 0.8, 0.8, 0.9, 0.7, 0.9, "street"
            ),
            "United States": Track(
                "United States", 84.0, 0.4, 0.6, 0.7, 0.8, 0.7, "permanent"
            ),
            "Mexico": Track(
                "Mexico", 86.0, 0.3, 0.7, 0.8, 0.7, 0.7, "permanent"
            ),
            "Brazil": Track(
                "Brazil", 85.0, 0.4, 0.6, 0.7, 0.8, 0.7, "permanent"
            ),
            "Las Vegas": Track(
                "Las Vegas", 90.0, 0.4, 0.7, 0.8, 0.5, 0.8, "street"
            ),
            "Qatar": Track(
                "Qatar", 88.0, 0.5, 0.8, 0.8, 0.6, 0.8, "permanent"
            ),
            "Abu Dhabi": Track(
                "Abu Dhabi", 84.0, 0.4, 0.6, 0.6, 0.5, 0.7, "permanent"
            )
        }
    
    def simulate_qualifying(self, track_name: str, num_simulations: int = 1000) -> List[List[Tuple[str, float]]]:
        """Realistic qualifying simulation"""
        track = self.tracks[track_name]
        qualifying_results = []
        
        for _ in range(num_simulations):
            driver_times = []
            
            for driver_name, driver in self.drivers.items():
                car = self.cars[driver.team]
                
                # Base qualifying time
                base_time = track.base_qualifying_time
                
                # Driver skill adjustment (better drivers = faster times)
                driver_skill_bonus = (100 - driver.raw_pace) * 0.03  # Max ~3s difference
                
                # Consistency factor (more consistent = less variance)
                consistency_variance = (1 - driver.consistency) * 2.0  # ±2s for inconsistent drivers
                consistency_adjustment = np.random.normal(0, consistency_variance)
                
                # Car performance adjustment
                car_performance = (car.aero_efficiency + car.engine_power) / 2
                car_bonus = (100 - car_performance) * 0.02  # Max ~2s difference
                
                # Track-specific adjustments
                if track.track_type == "street":
                    experience_bonus = driver.experience * 0.05  # Experience helps on street circuits
                else:
                    experience_bonus = 0
                
                # Current form adjustment
                form_adjustment = (driver.current_form - 1.0) * 1.0  # ±0.5s for form
                
                # Recent performance penalty (bad recent results = slower)
                recent_avg = np.mean(driver.recent_results)
                recent_penalty = (recent_avg - 10) * 0.1  # Bad results = penalty
                
                # Car upgrade factor
                car_upgrade = (1.0 - car.car_upgrade_factor) * 1.0
                
                # Weather adjustment
                weather_adjustment = 0
                if track.weather != WeatherCondition.DRY:
                    weather_adjustment = np.random.normal(1.0, 0.5)  # Rain adds time
                
                # Calculate final time
                final_time = (base_time + driver_skill_bonus + car_bonus + 
                            consistency_adjustment - experience_bonus + form_adjustment + 
                            recent_penalty + car_upgrade) * weather_adjustment
                
                driver_times.append((driver_name, final_time))
            
            # Sort by time (faster = better)
            driver_times.sort(key=lambda x: x[1])
            qualifying_results.append(driver_times)
        
        return qualifying_results
    
    def simulate_race(self, track_name: str, qualifying_results: List[List[Tuple[str, float]]], 
                     num_simulations: int = 1000) -> List[List[str]]:
        """Realistic race simulation with tire strategy, pit stops, DNFs, etc."""
        track = self.tracks[track_name]
        race_results = []
        
        for sim in range(num_simulations):
            # Get starting grid from qualifying
            starting_grid = [driver for driver, _ in qualifying_results[sim]]
            final_positions = starting_grid.copy()
            
            # Initialize tire strategies for each driver
            tire_strategies = {}
            for driver_name in final_positions:
                # Random tire strategy (soft/medium/hard)
                compounds = [TireCompound.SOFT, TireCompound.MEDIUM, TireCompound.HARD]
                tire_strategies[driver_name] = TireStrategy(
                    compound=random.choice(compounds),
                    age=0,
                    wear=0.0,
                    temperature=track.temperature
                )
            
            # Race simulation (50 laps)
            for lap in range(50):
                # Check for DNFs
                for i, driver_name in enumerate(final_positions):
                    if driver_name in self.drivers:
                        driver = self.drivers[driver_name]
                        car = self.cars[driver.team]
                        
                        # DNF probability based on reliability and driver skill
                        dnf_prob = (1 - car.reliability) * 0.001 + (1 - driver.physical_fitness / 100) * 0.0005
                        
                        if np.random.random() < dnf_prob:
                            final_positions.remove(driver_name)
                            final_positions.append(driver_name)  # Move to back
                
                # Tire wear and pit stops
                for driver_name in final_positions:
                    if driver_name in tire_strategies:
                        tire = tire_strategies[driver_name]
                        driver = self.drivers[driver_name]
                        car = self.cars[driver.team]
                        
                        # Increase tire wear
                        tire.age += 1
                        wear_rate = track.tire_wear_rate * car.tire_degradation * (1 - driver.tire_management / 100)
                        tire.wear += wear_rate
                        
                        # Pit stop if tires are worn
                        if tire.wear > 0.8 and np.random.random() < 0.3:  # 30% chance to pit when worn
                            # Change tires
                            new_compounds = [TireCompound.SOFT, TireCompound.MEDIUM, TireCompound.HARD]
                            tire.compound = random.choice(new_compounds)
                            tire.age = 0
                            tire.wear = 0.0
                
                # Overtaking simulation
                for i in range(len(final_positions) - 1):
                    if i >= len(final_positions) - 1:
                        break
                    
                    driver_ahead_name = final_positions[i]
                    driver_behind_name = final_positions[i + 1]
                    
                    if (driver_ahead_name in self.drivers and 
                        driver_behind_name in self.drivers):
                        
                        driver_ahead = self.drivers[driver_ahead_name]
                        driver_behind = self.drivers[driver_behind_name]
                        car_ahead = self.cars[driver_ahead.team]
                        car_behind = self.cars[driver_behind.team]
                        
                        # Calculate pace difference
                        pace_diff = (driver_behind.raw_pace - driver_ahead.raw_pace) / 100
                        car_pace_diff = (car_behind.aero_efficiency - car_ahead.aero_efficiency) / 100
                        
                        # Tire wear effect
                        tire_ahead = tire_strategies.get(driver_ahead_name)
                        tire_behind = tire_strategies.get(driver_behind_name)
                        
                        tire_advantage = 0
                        if tire_ahead and tire_behind:
                            tire_advantage = (tire_ahead.wear - tire_behind.wear) * 0.5
                        
                        # Overtaking probability
                        base_overtake_prob = 0.02  # 2% base chance
                        pace_overtake_prob = (pace_diff + car_pace_diff + tire_advantage) * 0.1
                        race_craft_bonus = (driver_behind.race_craft - driver_ahead.race_craft) / 100 * 0.05
                        
                        # Track difficulty reduces overtaking
                        track_factor = 1 - track.overtaking_difficulty
                        
                        total_overtake_prob = (base_overtake_prob + pace_overtake_prob + 
                                             race_craft_bonus) * track_factor
                        
                        # Safety car effect (increases overtaking)
                        if np.random.random() < 0.05:  # 5% chance of safety car
                            total_overtake_prob *= 2
                        
                        if np.random.random() < total_overtake_prob:
                            final_positions[i], final_positions[i + 1] = final_positions[i + 1], final_positions[i]
            
            race_results.append(final_positions)
        
        return race_results
    
    def run_monte_carlo_simulation(self, track_name: str, num_simulations: int = 10000) -> Dict:
        """Run complete Monte Carlo simulation"""
        print(f"Running realistic F1 simulation for {track_name}...")
        print(f"Number of simulations: {num_simulations}")
        
        # Simulate qualifying
        qualifying_results = self.simulate_qualifying(track_name, num_simulations)
        
        # Simulate race
        race_results = self.simulate_race(track_name, qualifying_results, num_simulations)
        
        # Calculate probabilities
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
            "race_results": race_results[:100]  # Store first 100 for analysis
        }
        
        self.results.append(results)
        return results
    
    def _calculate_win_probabilities(self, race_results: List[List[str]]) -> Dict[str, float]:
        """Calculate win probabilities"""
        win_counts = {driver: 0 for driver in self.drivers.keys()}
        total_races = len(race_results)
        
        for race in race_results:
            if race:
                winner = race[0]
                if winner in win_counts:
                    win_counts[winner] += 1
        
        return {driver: count / total_races for driver, count in win_counts.items()}
    
    def _calculate_podium_probabilities(self, race_results: List[List[str]]) -> Dict[str, float]:
        """Calculate podium probabilities"""
        podium_counts = {driver: 0 for driver in self.drivers.keys()}
        total_races = len(race_results)
        
        for race in race_results:
            for i, driver in enumerate(race[:3]):
                if driver in podium_counts:
                    podium_counts[driver] += 1
        
        return {driver: count / total_races for driver, count in podium_counts.items()}
    
    def _calculate_points_probabilities(self, race_results: List[List[str]]) -> Dict[str, float]:
        """Calculate points probabilities (top 10)"""
        points_counts = {driver: 0 for driver in self.drivers.keys()}
        total_races = len(race_results)
        
        for race in race_results:
            for i, driver in enumerate(race[:10]):
                if driver in points_counts:
                    points_counts[driver] += 1
        
        return {driver: count / total_races for driver, count in points_counts.items()}
    
    def get_prediction_summary(self, results: Dict) -> str:
        """Generate summary of simulation results"""
        win_probs = results["win_probabilities"]
        podium_probs = results["podium_probabilities"]
        
        # Top 5 most likely winners
        sorted_winners = sorted(win_probs.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = f"Realistic F1 2025 Race Prediction - {results['track']}\n"
        summary += f"Based on {results['num_simulations']:,} Monte Carlo simulations\n\n"
        summary += "Top 5 Most Likely Winners:\n"
        
        for i, (driver, prob) in enumerate(sorted_winners, 1):
            podium_prob = podium_probs[driver]
            team = self.drivers[driver].team
            championship_pos = self.drivers[driver].championship_position
            points = self.drivers[driver].championship_points
            summary += f"{i}. {driver} ({team}): {prob:.1%} win, {podium_prob:.1%} podium\n"
            summary += f"   Championship: #{championship_pos} ({points} pts)\n"
        
        return summary

# Example usage
if __name__ == "__main__":
    # Create simulation instance
    f1_sim = F1RealisticSimulation()
    
    # Run simulation for upcoming races
    upcoming_races = ["Monaco", "Canada", "Spain", "Austria", "Great Britain"]
    
    for track in upcoming_races:
        print(f"\n{'='*60}")
        results = f1_sim.run_monte_carlo_simulation(track, num_simulations=5000)
        
        # Print summary
        summary = f1_sim.get_prediction_summary(results)
        print(summary) 