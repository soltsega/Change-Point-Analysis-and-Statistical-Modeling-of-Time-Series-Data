# Assumptions and Limitations

## 🎯 Overview

This document outlines the key assumptions, limitations, and constraints of the change point analysis for Brent oil prices. Understanding these boundaries is crucial for proper interpretation of results and avoiding misinterpretation of statistical findings.

---

## 🔄 Correlation vs Causation

### **Critical Distinction**
- **Correlation**: Statistical relationship between two variables that move together
- **Causation**: Direct cause-and-effect relationship where one variable directly influences another

### **Our Analysis Limitations**
1. **Temporal Proximity ≠ Causation**: Just because a change point occurs near an event date doesn't prove the event caused the change
2. **Confounding Variables**: Multiple simultaneous events may influence oil prices
3. **Market Complexity**: Oil prices respond to countless factors beyond our event dataset

### **Causality Assessment Approach**
- **Temporal Analysis**: Verify event precedes price change
- **Plausibility Check**: Assess logical connection between event and market impact
- **Magnitude Assessment**: Evaluate if impact size matches event significance
- **Alternative Explanations**: Consider other potential causes

---

## 📊 Model Limitations

### **Change Point Model Constraints**
1. **Single Change Point Assumption**: Basic model assumes one structural break
   - **Reality**: Multiple change points likely exist
   - **Mitigation**: Consider hierarchical models for multiple change points

2. **Instantaneous Change Assumption**: Model assumes immediate regime shift
   - **Reality**: Market adjustments may be gradual
   - **Mitigation**: Examine transition periods and gradual changes

3. **Parameter Stationarity**: Assumes constant parameters within regimes
   - **Reality**: Volatility and trends may evolve within periods
   - **Mitigation**: Consider time-varying parameter models

### **Statistical Limitations**
1. **Sample Size**: Limited by available data period (2020-2026)
   - **Impact**: Reduced statistical power for rare events
   - **Mitigation**: Focus on frequent, high-impact events

2. **Distribution Assumptions**: Normal likelihood for price changes
   - **Reality**: Oil returns often exhibit fat tails
   - **Mitigation**: Consider Student-t or skewed distributions

---

## 📋 Data Limitations

### **Event Selection Bias**
1. **Major Event Focus**: Dataset emphasizes high-impact events
   - **Bias**: May overlook smaller cumulative effects
   - **Impact**: Overestimation of event importance
   - **Mitigation**: Include baseline market movements

2. **Retrospective Selection**: Events chosen with knowledge of outcomes
   - **Bias**: Hindsight bias in event importance
   - **Impact**: Inflated perceived predictability
   - **Mitigation**: Document selection criteria transparently

### **Temporal Constraints**
1. **Event Date Precision**: Single-day event timestamps
   - **Reality**: Events unfold over days/weeks
   - **Impact**: Misalignment with market reaction timing
   - **Mitigation**: Use event windows rather than precise dates

2. **Market Hours**: Global markets operate 24/7
   - **Reality**: Event timing affects immediate impact
   - **Impact**: Delayed reactions may be missed
   - **Mitigation**: Consider multi-day event windows

### **Data Quality Issues**
1. **Missing Data**: Weekends, holidays create gaps
   - **Impact**: Inconsistent time series
   - **Mitigation**: Use trading days only, acknowledge gaps

2. **Exchange Differences**: Brent vs WTI pricing
   - **Impact**: Regional market differences
   - **Mitigation**: Focus on Brent consistency

---

## 🌍 External Factors Not Modeled

### **Macroeconomic Variables**
1. **GDP Growth**: Economic expansion drives demand
2. **Inflation Rates**: Affects real oil prices
3. **Currency Exchange Rates**: USD strength impacts oil pricing
4. **Interest Rates**: Influence investment flows

### **Supply-Demand Dynamics**
1. **Production Levels**: OPEC+ output decisions
2. **Inventory Levels**: Strategic reserves affect supply
3. **Demand Seasonality**: Heating/cooling seasons
4. **Alternative Energy**: Renewable energy adoption

### **Geopolitical Factors**
1. **Regional Conflicts**: Beyond major wars
2. **Trade Relations**: Tariffs and agreements
3. **Regulatory Changes**: Environmental policies
4. **Technological Advances**: Extraction efficiency

---

## 📈 Interpretation Guidelines

### **What We Can Conclude**
1. **Statistical Change Points**: Identify significant price regime shifts
2. **Temporal Associations**: Events occurring near change points
3. **Magnitude Estimates**: Quantify price level changes
4. **Volatility Changes**: Assess risk regime shifts

### **What We Cannot Conclude**
1. **Definitive Causality**: Cannot prove events caused changes
2. **Predictive Power**: Cannot forecast future change points
3. **Comprehensive Analysis**: Cannot account for all market factors
4. **Policy Recommendations**: Cannot prescribe specific actions

### **Recommended Interpretation**
- **Probabilistic Language**: Use "likely associated with" rather than "caused by"
- **Confidence Intervals**: Report uncertainty in change point timing
- **Multiple Hypotheses**: Present alternative explanations
- **Contextual Factors**: Acknowledge broader market conditions

---

## 🔬 Validation Strategies

### **Robustness Checks**
1. **Alternative Windows**: Test different event time windows
2. **Model Variations**: Compare different change point models
3. **Bootstrap Analysis**: Assess result stability
4. **Cross-Validation**: Test on different time periods

### **Sensitivity Analysis**
1. **Event Inclusion**: Test with/without specific events
2. **Parameter Priors**: Assess prior sensitivity
3. **Time Horizons**: Vary analysis periods
4. **Market Conditions**: Stratify by volatility regimes

---

## 📝 Reporting Limitations

### **Transparency Requirements**
1. **Methodology Disclosure**: Complete model specification
2. **Assumption Documentation**: All assumptions clearly stated
3. **Uncertainty Quantification**: Confidence intervals for all estimates
4. **Alternative Explanations**: Acknowledge other possible causes

### **Communication Strategy**
1. **Clear Limitations Section**: Prominent in all reports
2. **Cautious Language**: Avoid definitive causal claims
3. **Visual Clarity**: Distinguish correlation from causation
4. **Stakeholder Education**: Explain statistical concepts

---

## 🎯 Conclusion

This change point analysis provides valuable insights into Brent oil price dynamics and their temporal association with major events. However, results must be interpreted with careful consideration of the assumptions and limitations outlined above. The analysis identifies statistical patterns and temporal relationships but cannot definitively establish causal mechanisms.

**Key Takeaway**: Use these results as one piece of evidence in a broader decision-making framework, complemented by fundamental analysis, market expertise, and consideration of broader economic context.
