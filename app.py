from flask import Flask, render_template, request, jsonify, send_file
import plotly.graph_objects as go
import plotly.utils
import json
import os
from f1_simulation_2025 import F1MonteCarloSimulation2025
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

app = Flask(__name__)
f1_sim = F1MonteCarloSimulation2025()

@app.route('/')
def index():
    """Main page with simulation interface"""
    tracks = list(f1_sim.tracks.keys())
    drivers = list(f1_sim.drivers.keys())
    teams = list(set([driver.team for driver in f1_sim.drivers.values()]))
    
    return render_template('index.html', tracks=tracks, drivers=drivers, teams=teams)

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    """Run Monte Carlo simulation and return results"""
    try:
        data = request.get_json()
        track_name = data.get('track', 'Silverstone')
        num_simulations = int(data.get('simulations', 5000))
        
        # Run simulation
        results = f1_sim.run_monte_carlo_simulation(track_name, num_simulations)
        
        # Generate summary
        summary = f1_sim.get_prediction_summary(results)
        
        # Create visualizations
        charts = create_interactive_charts(results)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'charts': charts,
            'results': {
                'win_probabilities': results['win_probabilities'],
                'podium_probabilities': results['podium_probabilities'],
                'points_probabilities': results['points_probabilities']
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def create_interactive_charts(results):
    """Create interactive Plotly charts"""
    charts = {}
    
    # Win probabilities chart
    win_probs = results['win_probabilities']
    drivers = list(win_probs.keys())
    probabilities = list(win_probs.values())
    
    # Sort by probability
    sorted_data = sorted(zip(drivers, probabilities), key=lambda x: x[1], reverse=True)
    drivers_sorted, probs_sorted = zip(*sorted_data)
    
    fig_win = go.Figure(data=[
        go.Bar(
            x=probs_sorted,
            y=drivers_sorted,
            orientation='h',
            marker_color='#FF6B6B',
            text=[f'{p:.1%}' for p in probs_sorted],
            textposition='auto'
        )
    ])
    
    fig_win.update_layout(
        title=f'Win Probabilities - {results["track"]}',
        xaxis_title='Win Probability',
        yaxis_title='Driver',
        height=600,
        showlegend=False
    )
    
    charts['win_chart'] = json.dumps(fig_win, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Podium probabilities chart
    podium_probs = results['podium_probabilities']
    podium_values = [podium_probs[driver] for driver in drivers_sorted]
    
    fig_podium = go.Figure(data=[
        go.Bar(
            x=podium_values,
            y=drivers_sorted,
            orientation='h',
            marker_color='#4ECDC4',
            text=[f'{p:.1%}' for p in podium_values],
            textposition='auto'
        )
    ])
    
    fig_podium.update_layout(
        title=f'Podium Probabilities - {results["track"]}',
        xaxis_title='Podium Probability',
        yaxis_title='Driver',
        height=600,
        showlegend=False
    )
    
    charts['podium_chart'] = json.dumps(fig_podium, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Team comparison chart
    team_win_probs = {}
    for driver, prob in win_probs.items():
        team = f1_sim.drivers[driver].team
        if team not in team_win_probs:
            team_win_probs[team] = 0
        team_win_probs[team] += prob
    
    teams = list(team_win_probs.keys())
    team_probs = list(team_win_probs.values())
    
    fig_team = go.Figure(data=[
        go.Pie(
            labels=teams,
            values=team_probs,
            textinfo='label+percent',
            insidetextorientation='radial'
        )
    ])
    
    fig_team.update_layout(
        title=f'Team Win Probabilities - {results["track"]}',
        height=500
    )
    
    charts['team_chart'] = json.dumps(fig_team, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

@app.route('/driver_stats/<driver_name>')
def driver_stats(driver_name):
    """Get detailed statistics for a specific driver"""
    if driver_name not in f1_sim.drivers:
        return jsonify({'error': 'Driver not found'})
    
    driver = f1_sim.drivers[driver_name]
    
    stats = {
        'name': driver.name,
        'team': driver.team,
        'base_speed': driver.base_speed,
        'consistency': driver.consistency,
        'qualifying_pace': driver.qualifying_pace,
        'race_pace': driver.race_pace,
        'reliability': driver.reliability,
        'experience': driver.experience,
        'current_form': driver.current_form,
        'championship_position': driver.championship_position,
        'points': driver.points,
        'recent_performance': driver.recent_performance,
        'car_news_factor': driver.car_news_factor,
        'engine_news_factor': driver.engine_news_factor
    }
    
    return jsonify(stats)

@app.route('/track_info/<track_name>')
def track_info(track_name):
    """Get information about a specific track"""
    if track_name not in f1_sim.tracks:
        return jsonify({'error': 'Track not found'})
    
    track = f1_sim.tracks[track_name]
    
    info = {
        'name': track_name,
        'type': track['type'],
        'overtaking_difficulty': track['overtaking_difficulty'],
        'technical_demand': track['technical_demand'],
        'weather_sensitivity': track['weather_sensitivity'],
        'tire_wear': track['tire_wear'],
        'season_round': track.get('season_round', 0)
    }
    
    return jsonify(info)

@app.route('/download_results', methods=['POST'])
def download_results():
    """Download simulation results as JSON"""
    try:
        data = request.get_json()
        track_name = data.get('track', 'Silverstone')
        num_simulations = int(data.get('simulations', 5000))
        
        # Run simulation
        results = f1_sim.run_monte_carlo_simulation(track_name, num_simulations)
        
        # Create JSON file
        output = io.StringIO()
        json.dump(results, output, indent=2, default=str)
        output.seek(0)
        
        return jsonify({
            'success': True,
            'data': output.getvalue(),
            'filename': f'f1_simulation_{track_name.lower()}.json'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 