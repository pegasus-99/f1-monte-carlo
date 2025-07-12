# 🏎️ F1 Monte Carlo Race Predictor

A sophisticated Monte Carlo simulation system that predicts F1 race winners using advanced statistical modeling and realistic driver/track characteristics.

## 🚀 Features

### Core Simulation Engine
- **Monte Carlo Simulation**: Runs thousands of race simulations to calculate win probabilities
- **Realistic Driver Modeling**: Each driver has individual characteristics:
  - Base speed and performance ratings
  - Consistency and reliability factors
  - Qualifying vs race pace differences
  - Experience and current form multipliers
- **Track-Specific Analysis**: Different tracks affect race outcomes based on:
  - Overtaking difficulty
  - Technical demands
  - Weather sensitivity
  - Tire wear characteristics

### Web Interface
- **Interactive Dashboard**: Beautiful, modern web interface
- **Real-time Simulations**: Run simulations with customizable parameters
- **Interactive Charts**: Plotly-powered visualizations
- **Results Export**: Download simulation results as JSON
- **Responsive Design**: Works on desktop and mobile devices

### Analysis Capabilities
- **Win Probabilities**: Percentage chance each driver wins
- **Podium Probabilities**: Likelihood of finishing in top 3
- **Points Probabilities**: Chance of scoring points (top 10)
- **Team Comparisons**: Aggregate team performance analysis
- **Statistical Summaries**: Detailed breakdown of results

## 📊 Current F1 Drivers Included

The simulation includes all current F1 drivers with realistic performance ratings:

| Driver | Team | Base Speed | Consistency | Qualifying | Race Pace | Reliability |
|--------|------|------------|-------------|------------|-----------|-------------|
| Max Verstappen | Red Bull | 95 | 0.90 | 96 | 97 | 0.95 |
| Lewis Hamilton | Mercedes | 93 | 0.92 | 94 | 93 | 0.93 |
| Charles Leclerc | Ferrari | 91 | 0.87 | 93 | 91 | 0.85 |
| Fernando Alonso | Aston Martin | 90 | 0.91 | 91 | 90 | 0.88 |
| George Russell | Mercedes | 89 | 0.88 | 90 | 89 | 0.88 |
| Sergio Perez | Red Bull | 88 | 0.85 | 89 | 90 | 0.90 |
| Carlos Sainz | Ferrari | 88 | 0.89 | 88 | 88 | 0.92 |
| Lando Norris | McLaren | 87 | 0.86 | 87 | 87 | 0.90 |
| Valtteri Bottas | Alfa Romeo | 86 | 0.87 | 87 | 86 | 0.89 |
| Daniel Ricciardo | AlphaTauri | 85 | 0.84 | 86 | 85 | 0.86 |
| Esteban Ocon | Alpine | 85 | 0.84 | 86 | 85 | 0.87 |
| Oscar Piastri | McLaren | 84 | 0.83 | 85 | 84 | 0.85 |
| Pierre Gasly | Alpine | 84 | 0.83 | 85 | 84 | 0.86 |
| Alexander Albon | Williams | 83 | 0.82 | 84 | 83 | 0.84 |
| Nico Hulkenberg | Haas | 83 | 0.81 | 84 | 83 | 0.83 |
| Kevin Magnussen | Haas | 82 | 0.80 | 83 | 82 | 0.84 |
| Lance Stroll | Aston Martin | 82 | 0.80 | 81 | 82 | 0.85 |
| Yuki Tsunoda | AlphaTauri | 81 | 0.79 | 82 | 81 | 0.81 |
| Zhou Guanyu | Alfa Romeo | 80 | 0.78 | 79 | 80 | 0.82 |
| Logan Sargeant | Williams | 78 | 0.75 | 77 | 78 | 0.80 |

## 🏁 Available Tracks

The simulation includes 5 major F1 circuits with unique characteristics:

| Track | Type | Overtaking | Technical | Weather | Tire Wear |
|-------|------|------------|-----------|---------|-----------|
| Monaco | Street Circuit | 0.90 | 0.95 | 0.80 | 0.70 |
| Silverstone | Permanent | 0.30 | 0.80 | 0.90 | 0.60 |
| Spa | Permanent | 0.40 | 0.90 | 0.95 | 0.50 |
| Monza | Permanent | 0.20 | 0.60 | 0.70 | 0.80 |
| Suzuka | Permanent | 0.50 | 0.90 | 0.80 | 0.70 |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd f1-monte-carlo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

### Web Interface
1. **Select a Track**: Choose from the available F1 circuits
2. **Set Simulations**: Adjust the number of Monte Carlo simulations (1000-50000)
3. **Run Simulation**: Click "Run Simulation" and wait for results
4. **View Results**: Analyze the interactive charts and statistics
5. **Download Data**: Export results as JSON for further analysis

### Command Line Usage
You can also run simulations directly from the command line:

```python
from f1_simulation import F1MonteCarloSimulation

# Create simulation instance
f1_sim = F1MonteCarloSimulation()

# Run simulation for a specific track
results = f1_sim.run_monte_carlo_simulation("Monaco", num_simulations=10000)

# Print summary
print(f1_sim.get_prediction_summary(results))

# Create visualizations
f1_sim.plot_results(results, save_path="monaco_prediction.png")
```

## 📈 Understanding the Results

### Win Probabilities
- Shows the percentage chance each driver has of winning the race
- Based on thousands of simulated races
- Accounts for qualifying performance, race pace, reliability, and track characteristics

### Podium Probabilities
- Likelihood of finishing in the top 3 positions
- Useful for betting and fantasy F1 leagues
- Reflects both speed and consistency

### Points Probabilities
- Chance of scoring championship points (top 10 finish)
- Important for championship standings
- Shows mid-field competitiveness

### Team Analysis
- Aggregate team performance
- Shows constructor championship implications
- Helps understand team strengths and weaknesses

## 🔬 How the Simulation Works

### Monte Carlo Method
The simulation uses the Monte Carlo method, which:
1. **Runs thousands of race simulations** with random variations
2. **Models realistic race dynamics** including qualifying, overtakes, and DNFs
3. **Calculates probabilities** based on the frequency of outcomes
4. **Provides statistical confidence** through large sample sizes

### Race Simulation Process
1. **Qualifying Simulation**: Determines starting grid based on driver pace and consistency
2. **Race Simulation**: Simulates 50 laps with:
   - Overtaking based on pace differences and track characteristics
   - DNFs based on reliability ratings
   - Position changes throughout the race
3. **Result Analysis**: Calculates win, podium, and points probabilities

### Driver Rating System
Each driver is rated on multiple dimensions:
- **Base Speed**: Overall performance potential
- **Consistency**: How reliable their performance is
- **Qualifying Pace**: Single-lap performance
- **Race Pace**: Long-run performance
- **Reliability**: Mechanical reliability factor
- **Experience**: Years in F1 (affects certain tracks)
- **Current Form**: Recent performance multiplier

## 🎨 Customization

### Adding New Drivers
Edit the `_initialize_drivers()` method in `f1_simulation.py`:

```python
"New Driver": Driver("New Driver", "Team Name", 85, 0.85, 86, 85, 0.88, 3, 1.0)
```

### Adding New Tracks
Edit the `_initialize_tracks()` method:

```python
"New Track": {
    "type": "permanent_circuit",
    "overtaking_difficulty": 0.5,
    "technical_demand": 0.8,
    "weather_sensitivity": 0.7,
    "tire_wear": 0.6
}
```

### Adjusting Driver Ratings
Modify driver characteristics to reflect current form or new data:

```python
# Update Max Verstappen's current form
self.drivers["Max Verstappen"].current_form = 1.3  # 30% boost
```

## 📊 Example Results

Here's what a typical simulation output looks like:

```
F1 Race Prediction - Monaco
Based on 10,000 Monte Carlo simulations

Top 5 Most Likely Winners:
1. Max Verstappen (Red Bull): 45.2% win, 78.5% podium
2. Charles Leclerc (Ferrari): 18.7% win, 65.3% podium
3. Lewis Hamilton (Mercedes): 12.3% win, 52.1% podium
4. Fernando Alonso (Aston Martin): 8.9% win, 45.7% podium
5. Lando Norris (McLaren): 6.2% win, 38.9% podium
```

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding more realistic driver ratings
- Including additional tracks
- Improving the simulation algorithms
- Enhancing the web interface
- Adding more statistical analysis features

## 📝 License

This project is open source and available under the MIT License.

## 🏆 Disclaimer

This simulation is for educational and entertainment purposes only. It should not be used for actual betting or gambling. F1 race outcomes depend on many unpredictable factors that cannot be fully modeled in a simulation.

## 📞 Support

If you have questions or suggestions, feel free to open an issue or contribute to the project!

---

**Happy Racing! 🏎️🏁** 