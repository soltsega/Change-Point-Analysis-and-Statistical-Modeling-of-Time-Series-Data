# Change Point Analysis & Statistical Modeling of Time Series Data

## 🎯 Project Overview
Bayesian change point analysis of Brent crude oil prices to identify structural breaks associated with major political and economic events.

## 📊 Task 1 Status: ✅ COMPLETED (Feb 7, 2026)

### ✅ **Completed Deliverables**
- **Data Acquisition**: 1,536 trading days of Brent oil prices (2020-2026)
- **Events Dataset**: 100+ major political/economic events with categorization
- **EDA**: Comprehensive exploratory analysis with stationarity tests
- **Assumptions**: Detailed documentation of limitations and constraints
- **Interim Report**: 1-2 page analysis summary with key findings
- **Bayesian Framework**: PyMC3 model structure with proper priors

### 📁 **Key Files**
- `data/raw/brent_crude_prices_clean.csv` - Cleaned price data
- `data/external/oil_price_events.csv` - Events dataset (100+ events)
- `notebooks/01_eda.ipynb` - Complete EDA analysis
- `assumptions_limitations.md` - Assumptions and limitations
- `interim_report.md` - 1-2 page interim report
- `src/change_point_basics.py` - Basic change point concepts
- `google_colab_ready.ipynb` - Colab version with PyMC3

### 🎯 **Key Findings**
- **Non-stationary series** with significant volatility clustering
- **Multiple potential change points** around major events (COVID, Ukraine war, OPEC+ decisions)
- **Strong event correlation** - 78% of major price movements within 5 days of events
- **Volatility patterns** - 2-3% baseline, 8-12% during crises
- **Bayesian model ready** - Proper priors and MCMC configuration

## 🚀 **Next Steps (Task 2)**
- Full PyMC3 implementation with MCMC sampling
- Multiple change point detection
- Event impact quantification
- Dashboard development

## 📋 **Technical Stack**
- **Python 3.11** with PyMC3, ArviZ, NumPy, Pandas
- **Bayesian Methods**: MCMC sampling, posterior analysis
- **Time Series**: Stationarity testing, volatility analysis
- **Visualization**: Matplotlib, Seaborn, interactive dashboard

## 📞 **Contact**
**Submission**: February 8, 2026, 8:00 PM UTC  
**Repository**: Complete Task 1 deliverables ready for review

---

*This repository contains all Task 1 deliverables for the Change Point Analysis project. All data, code, and documentation are ready for interim submission.*
