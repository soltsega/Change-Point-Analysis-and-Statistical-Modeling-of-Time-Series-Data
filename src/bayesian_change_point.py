"""
Bayesian Change Point Analysis - Simplified Implementation

This module implements change point detection using a Bayesian approach
without requiring PyMC3, which has compatibility issues with current NumPy version.

Uses scipy for optimization and matplotlib for visualization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats, optimize
from scipy.stats import norm, uniform
import warnings
warnings.filterwarnings('ignore')

class BayesianChangePoint:
    """
    Bayesian Change Point Detection using grid approximation
    Implements the same concepts as PyMC3 but with scipy for compatibility
    """
    
    def __init__(self, data, time_index=None):
        """
        Initialize with time series data
        
        Args:
            data: Array or Series of time series values
            time_index: Time labels (dates, etc.)
        """
        self.data = np.array(data)
        self.n = len(data)
        self.time_index = time_index if time_index is not None else np.arange(self.n)
        
        # Priors
        self.tau_prior_range = (self.n * 0.2, self.n * 0.8)  # Change point in middle 80%
        self.mu_prior_mean = np.mean(data)
        self.mu_prior_std = np.std(data) * 2
        self.sigma_prior_scale = np.std(data)
        
        # Results
        self.posterior_tau = None
        self.posterior_mu1 = None
        self.posterior_mu2 = None
        self.posterior_sigma = None
        self.map_estimate = None
        
    def calculate_posterior_grid(self, n_grid_points=100):
        """
        Calculate posterior distribution using grid approximation
        
        Args:
            n_grid_points: Number of grid points for each parameter
        """
        print("Calculating posterior distribution using grid approximation...")
        
        # Create parameter grids
        tau_grid = np.linspace(self.tau_prior_range[0], self.tau_prior_range[1], n_grid_points)
        mu1_grid = np.linspace(self.mu_prior_mean - 2*self.mu_prior_std, 
                               self.mu_prior_mean + 2*self.mu_prior_std, n_grid_points)
        mu2_grid = np.linspace(self.mu_prior_mean - 2*self.mu_prior_std, 
                               self.mu_prior_mean + 2*self.mu_prior_std, n_grid_points)
        sigma_grid = np.linspace(0.1, self.sigma_prior_scale * 2, n_grid_points)
        
        # Initialize posterior
        posterior = np.zeros((n_grid_points, n_grid_points, n_grid_points, n_grid_points))
        
        # Calculate posterior for each parameter combination
        for i, tau in enumerate(tau_grid):
            tau_int = int(tau)
            if tau_int <= 10 or tau_int >= self.n - 10:
                continue
                
            # Split data at change point
            before_data = self.data[:tau_int]
            after_data = self.data[tau_int:]
            
            for j, mu1 in enumerate(mu1_grid):
                for k, mu2 in enumerate(mu2_grid):
                    for l, sigma in enumerate(sigma_grid):
                        # Calculate log posterior
                        log_posterior = 0
                        
                        # Priors
                        log_posterior += np.log(uniform.pdf(tau, self.tau_prior_range[0], self.tau_prior_range[1]))
                        log_posterior += np.log(norm.pdf(mu1, self.mu_prior_mean, self.mu_prior_std))
                        log_posterior += np.log(norm.pdf(mu2, self.mu_prior_mean, self.mu_prior_std))
                        log_posterior += np.log(stats.halfcauchy.pdf(sigma, 0, self.sigma_prior_scale))
                        
                        # Likelihood
                        if sigma > 0:
                            # Before change point
                            if len(before_data) > 0:
                                log_posterior += np.sum(norm.logpdf(before_data, mu1, sigma))
                            # After change point  
                            if len(after_data) > 0:
                                log_posterior += np.sum(norm.logpdf(after_data, mu2, sigma))
                        
                        posterior[i, j, k, l] = log_posterior
        
        # Find MAP estimate
        max_idx = np.unravel_index(np.argmax(posterior), posterior.shape)
        self.map_estimate = {
            'tau': tau_grid[max_idx[0]],
            'mu1': mu1_grid[max_idx[1]],
            'mu2': mu2_grid[max_idx[2]],
            'sigma': sigma_grid[max_idx[3]],
            'log_posterior': posterior[max_idx]
        }
        
        # Calculate marginal posteriors
        self.posterior_tau = np.exp(posterior.sum(axis=(1, 2, 3)))
        self.posterior_tau /= self.posterior_tau.sum()
        
        self.posterior_mu1 = np.exp(posterior.sum(axis=(0, 2, 3)))
        self.posterior_mu1 /= self.posterior_mu1.sum()
        
        self.posterior_mu2 = np.exp(posterior.sum(axis=(0, 1, 3)))
        self.posterior_mu2 /= self.posterior_mu2.sum()
        
        print(f"MAP Estimate: tau={self.map_estimate['tau']:.0f}, mu1={self.map_estimate['mu1']:.2f}, mu2={self.map_estimate['mu2']:.2f}")
        
        return self.map_estimate
    
    def calculate_posterior_mcmc(self, n_samples=10000, burn_in=1000):
        """
        Simplified MCMC implementation for change point detection
        Uses Metropolis-Hastings algorithm
        """
        print("Running MCMC sampling...")
        
        # Initialize parameters
        current_tau = self.n // 2
        current_mu1 = np.mean(self.data[:current_tau])
        current_mu2 = np.mean(self.data[current_tau:])
        current_sigma = np.std(self.data)
        
        # Storage for samples
        tau_samples = []
        mu1_samples = []
        mu2_samples = []
        sigma_samples = []
        
        # MCMC parameters
        tau_step = 5
        mu_step = 1.0
        sigma_step = 0.5
        
        for iteration in range(n_samples + burn_in):
            # Propose new parameters
            new_tau = np.clip(current_tau + np.random.randint(-tau_step, tau_step + 1), 10, self.n - 10)
            new_mu1 = current_mu1 + np.random.normal(0, mu_step)
            new_mu2 = current_mu2 + np.random.normal(0, mu_step)
            new_sigma = abs(current_sigma + np.random.normal(0, sigma_step))
            
            # Calculate log posterior for current and proposed
            current_log_post = self._log_posterior(current_tau, current_mu1, current_mu2, current_sigma)
            new_log_post = self._log_posterior(new_tau, new_mu1, new_mu2, new_sigma)
            
            # Accept/reject
            log_ratio = new_log_post - current_log_post
            if np.log(np.random.random()) < log_ratio:
                current_tau, current_mu1, current_mu2, current_sigma = new_tau, new_mu1, new_mu2, new_sigma
            
            # Store samples after burn-in
            if iteration >= burn_in:
                tau_samples.append(current_tau)
                mu1_samples.append(current_mu1)
                mu2_samples.append(current_mu2)
                sigma_samples.append(current_sigma)
            
            # Progress
            if iteration % 1000 == 0:
                print(f"Iteration {iteration}/{n_samples + burn_in}")
        
        # Convert to arrays
        self.posterior_tau = np.array(tau_samples)
        self.posterior_mu1 = np.array(mu1_samples)
        self.posterior_mu2 = np.array(mu2_samples)
        self.posterior_sigma = np.array(sigma_samples)
        
        # Calculate convergence statistics
        self.map_estimate = {
            'tau': np.mean(self.posterior_tau),
            'mu1': np.mean(self.posterior_mu1),
            'mu2': np.mean(self.posterior_mu2),
            'sigma': np.mean(self.posterior_sigma)
        }
        
        # Calculate R-hat (Gelman-Rubin statistic)
        # Split chains and calculate between/within variance
        n_chains = 4
        chain_length = len(self.posterior_tau) // n_chains
        
        r_hat_tau = self._calculate_r_hat(self.posterior_tau, n_chains)
        r_hat_mu1 = self._calculate_r_hat(self.posterior_mu1, n_chains)
        r_hat_mu2 = self._calculate_r_hat(self.posterior_mu2, n_chains)
        
        print(f"MCMC Convergence:")
        print(f"R-hat (tau): {r_hat_tau:.4f}")
        print(f"R-hat (mu1): {r_hat_mu1:.4f}")
        print(f"R-hat (mu2): {r_hat_mu2:.4f}")
        
        return self.map_estimate
    
    def _log_posterior(self, tau, mu1, mu2, sigma):
        """Calculate log posterior for given parameters"""
        tau_int = int(tau)
        if tau_int <= 10 or tau_int >= self.n - 10 or sigma <= 0:
            return -np.inf
        
        # Split data
        before_data = self.data[:tau_int]
        after_data = self.data[tau_int:]
        
        log_post = 0
        
        # Priors
        log_post += np.log(uniform.pdf(tau, self.tau_prior_range[0], self.tau_prior_range[1]))
        log_post += np.log(norm.pdf(mu1, self.mu_prior_mean, self.mu_prior_std))
        log_post += np.log(norm.pdf(mu2, self.mu_prior_mean, self.mu_prior_std))
        log_post += np.log(stats.halfcauchy.pdf(sigma, 0, self.sigma_prior_scale))
        
        # Likelihood
        if len(before_data) > 0:
            log_post += np.sum(norm.logpdf(before_data, mu1, sigma))
        if len(after_data) > 0:
            log_post += np.sum(norm.logpdf(after_data, mu2, sigma))
        
        return log_post
    
    def _calculate_r_hat(self, samples, n_chains):
        """Calculate Gelman-Rubin R-hat statistic"""
        if len(samples) < n_chains * 2:
            return 1.0  # Not enough samples
        
        # Split into chains
        chain_length = len(samples) // n_chains
        chains = samples[:n_chains*chain_length].reshape(n_chains, chain_length)
        
        # Calculate within-chain variance
        within_var = np.mean([np.var(chain) for chain in chains])
        
        # Calculate between-chain variance
        chain_means = np.mean(chains, axis=1)
        between_var = chain_length * np.var(chain_means)
        
        # Calculate R-hat
        total_var = (1 - 1/chain_length) * within_var + (1/chain_length) * between_var
        r_hat = np.sqrt(total_var / within_var)
        
        return r_hat
    
    def plot_results(self):
        """Plot comprehensive change point analysis results"""
        if self.map_estimate is None:
            print("Run analysis first!")
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Bayesian Change Point Analysis Results', fontsize=16, fontweight='bold')
        
        # Plot 1: Original data with change point
        axes[0,0].plot(self.time_index, self.data, 'b-', alpha=0.7, linewidth=2)
        tau_idx = int(self.map_estimate['tau'])
        axes[0,0].axvline(x=self.time_index[tau_idx], color='red', linestyle='--', 
                         linewidth=3, label=f'Change Point')
        axes[0,0].axhline(y=self.map_estimate['mu1'], color='green', linestyle=':', 
                         linewidth=2, label=f'Before Mean: ${self.map_estimate["mu1"]:.2f}')
        axes[0,0].axhline(y=self.map_estimate['mu2'], color='orange', linestyle=':', 
                         linewidth=2, label=f'After Mean: ${self.map_estimate["mu2"]:.2f}')
        axes[0,0].set_title('Time Series with Detected Change Point', fontsize=12)
        axes[0,0].set_xlabel('Time')
        axes[0,0].set_ylabel('Price (USD)')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # Plot 2: Posterior of tau
        if hasattr(self, 'posterior_tau') and len(self.posterior_tau) > 0:
            axes[0,1].hist(self.posterior_tau, bins=50, density=True, alpha=0.7, color='red', edgecolor='black')
            axes[0,1].axvline(x=self.map_estimate['tau'], color='darkred', linestyle='--', 
                             linewidth=2, label=f'MAP: {self.map_estimate["tau"]:.0f}')
            axes[0,1].set_title('Posterior Distribution of Change Point (τ)', fontsize=12)
            axes[0,1].set_xlabel('Change Point Position')
            axes[0,1].set_ylabel('Density')
            axes[0,1].legend()
            axes[0,1].grid(True, alpha=0.3)
        
        # Plot 3: Before vs After distributions
        tau_idx = int(self.map_estimate['tau'])
        before_data = self.data[:tau_idx]
        after_data = self.data[tau_idx:]
        
        axes[0,2].hist(before_data, bins=30, alpha=0.5, label='Before Change', 
                      color='blue', density=True)
        axes[0,2].hist(after_data, bins=30, alpha=0.5, label='After Change', 
                      color='red', density=True)
        axes[0,2].axvline(x=self.map_estimate['mu1'], color='blue', linestyle='--', 
                         linewidth=2, label=f'Before Mean: ${self.map_estimate["mu1"]:.2f}')
        axes[0,2].axvline(x=self.map_estimate['mu2'], color='red', linestyle='--', 
                         linewidth=2, label=f'After Mean: ${self.map_estimate["mu2"]:.2f}')
        axes[0,2].set_title('Distribution Comparison', fontsize=12)
        axes[0,2].set_xlabel('Price (USD)')
        axes[0,2].set_ylabel('Density')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
        
        # Plot 4: Posterior of mu1
        if hasattr(self, 'posterior_mu1') and len(self.posterior_mu1) > 0:
            axes[1,0].hist(self.posterior_mu1, bins=30, density=True, alpha=0.7, 
                          color='green', edgecolor='black')
            axes[1,0].axvline(x=self.map_estimate['mu1'], color='darkgreen', linestyle='--', 
                             linewidth=2, label=f'MAP: ${self.map_estimate["mu1"]:.2f}')
            axes[1,0].set_title('Posterior of Before Mean (μ₁)', fontsize=12)
            axes[1,0].set_xlabel('Mean Value (USD)')
            axes[1,0].set_ylabel('Density')
            axes[1,0].legend()
            axes[1,0].grid(True, alpha=0.3)
        
        # Plot 5: Posterior of mu2
        if hasattr(self, 'posterior_mu2') and len(self.posterior_mu2) > 0:
            axes[1,1].hist(self.posterior_mu2, bins=30, density=True, alpha=0.7, 
                          color='orange', edgecolor='black')
            axes[1,1].axvline(x=self.map_estimate['mu2'], color='darkorange', linestyle='--', 
                             linewidth=2, label=f'MAP: ${self.map_estimate["mu2"]:.2f}')
            axes[1,1].set_title('Posterior of After Mean (μ₂)', fontsize=12)
            axes[1,1].set_xlabel('Mean Value (USD)')
            axes[1,1].set_ylabel('Density')
            axes[1,1].legend()
            axes[1,1].grid(True, alpha=0.3)
        
        # Plot 6: Summary statistics
        axes[1,2].axis('off')
        summary_text = f"""
        BAYESIAN CHANGE POINT SUMMARY
        
        Change Point (τ): {self.map_estimate['tau']:.0f}
        Date: {self.time_index[tau_idx] if hasattr(self.time_index, '__getitem__') else 'N/A'}
        
        Before Mean (μ₁): ${self.map_estimate['mu1']:.2f}
        After Mean (μ₂): ${self.map_estimate['mu2']:.2f}
        
        Price Change: ${abs(self.map_estimate['mu2'] - self.map_estimate['mu1']):.2f}
        Percent Change: {(self.map_estimate['mu2'] - self.map_estimate['mu1']) / abs(self.map_estimate['mu1']) * 100:.1f}%
        
        Before Std: ${np.std(before_data):.2f}
        After Std: ${np.std(after_data):.2f}
        
        Volatility Change: {(np.std(after_data) - np.std(before_data)) / np.std(before_data) * 100:.1f}%
        """
        
        axes[1,2].text(0.1, 0.9, summary_text, fontsize=10, 
                      verticalalignment='top', fontfamily='monospace')
        axes[1,2].set_title('Summary Statistics', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        # Print detailed results
        print("\n" + "="*60)
        print("BAYESIAN CHANGE POINT ANALYSIS RESULTS")
        print("="*60)
        print(f"Change Point (τ): Index {self.map_estimate['tau']:.0f}")
        print(f"Before Mean (μ₁): ${self.map_estimate['mu1']:.4f}")
        print(f"After Mean (μ₂): ${self.map_estimate['mu2']:.4f}")
        print(f"Price Change: ${abs(self.map_estimate['mu2'] - self.map_estimate['mu1']):.4f}")
        print(f"Percent Change: {(self.map_estimate['mu2'] - self.map_estimate['mu1']) / abs(self.map_estimate['mu1']) * 100:.2f}%")
        print(f"Before Std Dev: ${np.std(before_data):.4f}")
        print(f"After Std Dev: ${np.std(after_data):.4f}")
        print(f"Volatility Change: {(np.std(after_data) - np.std(before_data)) / np.std(before_data) * 100:.2f}%")

def analyze_brent_oil_prices():
    """Example function to analyze Brent oil prices"""
    print("Loading Brent oil price data...")
    
    # Load data
    df = pd.read_csv('../data/raw/brent_crude_prices_clean.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Use closing prices
    prices = df['Close'].values
    dates = df['Date'].values
    
    print(f"Data loaded: {len(prices)} trading days")
    print(f"Date range: {dates[0]} to {dates[-1]}")
    print(f"Price range: ${prices.min():.2f} - ${prices.max():.2f}")
    
    # Run Bayesian change point analysis
    bcp = BayesianChangePoint(prices, dates)
    
    # Use MCMC for better results
    results = bcp.calculate_posterior_mcmc(n_samples=5000, burn_in=1000)
    
    # Plot results
    bcp.plot_results()
    
    return bcp, results

if __name__ == "__main__":
    # Run the analysis
    bcp_analyzer, results = analyze_brent_oil_prices()
