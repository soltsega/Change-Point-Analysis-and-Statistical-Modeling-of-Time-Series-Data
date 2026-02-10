"""
Flask Backend for Change Point Analysis Dashboard
API endpoints for data, visualizations, and analysis results
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__, template_folder='templates')
CORS(app)

# Global variables for cached data
data_cache = {}
events_cache = {}
change_point_cache = {}

def load_data():
    """Load and cache data files"""
    global data_cache, events_cache, change_point_cache
    
    try:
        # Load processed data
        data_path = os.path.join('..', 'data', 'processed', 'brent_processed.csv')
        if os.path.exists(data_path):
            data_cache = pd.read_csv(data_path)
            data_cache['Date'] = pd.to_datetime(data_cache['Date'])
            data_cache['Log_Returns'] = np.log(data_cache['Close'] / data_cache['Close'].shift(1))
            data_cache = data_cache.dropna().reset_index(drop=True)
            print(f"✅ Loaded {len(data_cache)} data points")
        else:
            # Generate sample data if file not found
            dates = pd.date_range('2020-01-01', '2026-02-06', freq='B')
            prices = 50 + np.cumsum(np.random.normal(0, 2, len(dates)))
            data_cache = pd.DataFrame({
                'Date': dates,
                'Close': prices,
                'Log_Returns': np.log(prices / np.roll(prices, 1))[1:]
            })
            data_cache = data_cache.dropna().reset_index(drop=True)
            print("🔄 Using sample data")
        
        # Load events data
        events_path = os.path.join('..', 'data', 'external', 'oil_price_events.csv')
        if os.path.exists(events_path):
            events_cache = pd.read_csv(events_path)
            events_cache['Date'] = pd.to_datetime(events_cache['Date'])
            print(f"✅ Loaded {len(events_cache)} events")
        else:
            # Generate sample events
            events_cache = pd.DataFrame({
                'Date': pd.date_range('2021-01-01', '2025-12-31', freq='6M'),
                'Event': [f'Major Event {i+1}' for i in range(8)],
                'Impact': ['High', 'Medium', 'Extreme', 'High', 'Medium', 'High', 'Extreme', 'Medium']
            })
            print("🔄 Using sample events")
        
        # Calculate change point (simplified version)
        returns = data_cache['Log_Returns'].values
        T = len(returns)
        tau_candidates = np.linspace(T//4, 3*T//4, 100, dtype=int)
        
        log_likelihoods = []
        for tau in tau_candidates:
            y1 = returns[:tau]
            y2 = returns[tau:]
            mu1, sigma1 = np.mean(y1), np.std(y1)
            mu2, sigma2 = np.mean(y2), np.std(y2)
            
            from scipy import stats
            ll1 = np.sum(stats.norm.logpdf(y1, mu1, sigma1))
            ll2 = np.sum(stats.norm.logpdf(y2, mu2, sigma2))
            log_likelihoods.append(ll1 + ll2)
        
        best_idx = np.argmax(log_likelihoods)
        tau_best = tau_candidates[best_idx]
        
        change_point_cache = {
            'tau': int(tau_best),
            'date': data_cache['Date'].iloc[tau_best].strftime('%Y-%m-%d'),
            'mu1': float(np.mean(returns[:tau_best])),
            'mu2': float(np.mean(returns[tau_best:])),
            'sigma1': float(np.std(returns[:tau_best])),
            'sigma2': float(np.std(returns[tau_best:])),
            'mean_shift': float(np.mean(returns[tau_best:]) - np.mean(returns[:tau_best])),
            'volatility_change': float((np.std(returns[tau_best:]) - np.std(returns[:tau_best])) / np.std(returns[:tau_best]) * 100)
        }
        
        print(f"✅ Change point calculated: Day {tau_best}")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")

@app.route('/')
def index():
    """Serve HTML dashboard"""
    from flask import render_template
    return render_template('index.html')

@app.route('/test')
def test():
    """Test route"""
    from flask import send_from_directory
    return send_from_directory('.', 'test.html')

@app.route('/api/data')
def get_data():
    """Get time series data"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        df = data_cache.copy()
        
        # Filter by date range if provided
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        
        # Convert to JSON
        data = {
            'dates': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'prices': df['Close'].tolist(),
            'log_returns': df['Log_Returns'].tolist()
        }
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events')
def get_events():
    """Get events data"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        df = events_cache.copy()
        
        # Filter by date range if provided
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        
        # Convert to JSON
        data = {
            'events': []
        }
        
        for _, event in df.iterrows():
            event_data = {
                'date': event['Date'].strftime('%Y-%m-%d'),
                'event': event.get('Event', 'Unknown Event'),
                'impact': event.get('Impact', 'Unknown')
            }
            data['events'].append(event_data)
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/change-point')
def get_change_point():
    """Get change point analysis results"""
    try:
        return jsonify(change_point_cache)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis')
def get_analysis():
    """Get comprehensive analysis results"""
    try:
        # Get query parameters
        window_size = int(request.args.get('window_size', 30))
        
        # Calculate rolling statistics
        df = data_cache.copy()
        df['Rolling_Mean'] = df['Close'].rolling(window=window_size).mean()
        df['Rolling_Std'] = df['Close'].rolling(window=window_size).std()
        df['Rolling_Volatility'] = df['Log_Returns'].rolling(window=window_size).std()
        
        # Calculate volatility percentiles
        vol_threshold = np.percentile(np.abs(df['Log_Returns']), 90)
        df['High_Volatility'] = np.abs(df['Log_Returns']) > vol_threshold
        
        # Convert to JSON
        data = {
            'dates': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'prices': df['Close'].tolist(),
            'rolling_mean': df['Rolling_Mean'].fillna(0).tolist(),
            'rolling_std': df['Rolling_Std'].fillna(0).tolist(),
            'rolling_volatility': df['Rolling_Volatility'].fillna(0).tolist(),
            'high_volatility': df['High_Volatility'].tolist(),
            'volatility_threshold': float(vol_threshold),
            'window_size': window_size
        }
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualizations')
def get_visualizations():
    """Get pre-computed visualization data"""
    try:
        viz_data = {
            'change_point': change_point_cache,
            'summary_stats': {
                'total_observations': len(data_cache),
                'date_range': {
                    'start': data_cache['Date'].min().strftime('%Y-%m-%d'),
                    'end': data_cache['Date'].max().strftime('%Y-%m-%d')
                },
                'price_stats': {
                    'min': float(data_cache['Close'].min()),
                    'max': float(data_cache['Close'].max()),
                    'mean': float(data_cache['Close'].mean()),
                    'std': float(data_cache['Close'].std())
                },
                'returns_stats': {
                    'mean': float(data_cache['Log_Returns'].mean()),
                    'std': float(data_cache['Log_Returns'].std()),
                    'min': float(data_cache['Log_Returns'].min()),
                    'max': float(data_cache['Log_Returns'].max())
                }
            }
        }
        
        return jsonify(viz_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_loaded': len(data_cache) > 0,
        'events_loaded': len(events_cache) > 0,
        'change_point_calculated': len(change_point_cache) > 0
    })

if __name__ == '__main__':
    print("🚀 Starting Flask Backend...")
    load_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
