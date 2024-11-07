import os
from experiment_runner import run_experiments
from results_visualization import visualize_results

def main():
    # Create directories if they don't exist
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # Define parameters
    max_n = 1000  # Adjust based on computational resources
    densities = [0.125, 0.25, 0.5, 0.75]
    seed = 102620 
    # Run experiments
    run_experiments(max_n, densities, seed)
    # Visualize results
    visualize_results()

if __name__ == '__main__':
    main()
