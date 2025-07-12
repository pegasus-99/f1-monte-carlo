#!/usr/bin/env python3
"""
F1 Monte Carlo Simulation Demo
Quick demonstration of the simulation capabilities
"""

from f1_simulation import F1MonteCarloSimulation
import time

def main():
    print("🏎️ F1 Monte Carlo Race Predictor Demo")
    print("=" * 50)
    
    # Create simulation instance
    f1_sim = F1MonteCarloSimulation()
    
    # Demo tracks
    tracks = ["Monaco", "Silverstone", "Spa"]
    
    for track in tracks:
        print(f"\n🏁 Simulating {track} Grand Prix...")
        print("-" * 30)
        
        # Run simulation with fewer iterations for demo
        start_time = time.time()
        results = f1_sim.run_monte_carlo_simulation(track, num_simulations=2000)
        end_time = time.time()
        
        # Print summary
        summary = f1_sim.get_prediction_summary(results)
        print(summary)
        
        # Show top 3 drivers with their probabilities
        win_probs = results['win_probabilities']
        sorted_winners = sorted(win_probs.items(), key=lambda x: x[1], reverse=True)[:3]
        
        print("🏆 Top 3 Predicted Winners:")
        for i, (driver, prob) in enumerate(sorted_winners, 1):
            team = f1_sim.drivers[driver].team
            podium_prob = results['podium_probabilities'][driver]
            print(f"  {i}. {driver} ({team})")
            print(f"     Win: {prob:.1%} | Podium: {podium_prob:.1%}")
        
        print(f"\n⏱️  Simulation completed in {end_time - start_time:.2f} seconds")
        print("=" * 50)
    
    print("\n🎯 Demo completed! Run 'python app.py' to use the web interface.")
    print("📊 For more detailed analysis, increase the number of simulations.")

if __name__ == "__main__":
    main() 