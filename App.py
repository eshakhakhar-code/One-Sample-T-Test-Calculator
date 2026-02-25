import streamlit as st
import numpy as np
from scipy.stats import t

def ttest(data, mu0, alpha=0.05, alternative="two-sided"):
    data = np.array(data)
    n = len(data)
    xbar = np.mean(data)
    s = np.std(data, ddof=1)
    se = s / np.sqrt(n)
    t_cal = (xbar - mu0) / se
    df = n - 1

    if alternative == "two-sided":
        t_crit = t.ppf(1 - alpha/2, df)
        p_value = 2 * (1 - t.cdf(abs(t_cal), df))
        reject = abs(t_cal) > t_crit
    elif alternative == "greater":
        t_crit = t.ppf(1 - alpha, df)
        p_value = 1 - t.cdf(t_cal, df)
        reject = t_cal > t_crit
    elif alternative == "less":
        t_crit = t.ppf(alpha, df)
        p_value = t.cdf(t_cal, df)
        reject = t_cal < t_crit

    return {
        "xbar": xbar, "s": s, "t_cal": t_cal, 
        "df": df, "p_value": p_value, 
        "decision": "Reject Null Hypothesis" if reject else "Fail to Reject Null Hypothesis"
    }


st.title("📊 One-Sample T-Test Calculator")

tab1, tab2 = st.tabs(["Input Data", "Results"])

with tab1:
    st.subheader("Configure Test Parameters")
    
    # Data Input
    raw_data = st.text_input("Enter data points (comma-separated)", "10, 12, 9, 11, 12, 10, 8, 13")
    
    col1, col2 = st.columns(2)
    with col1:
        mu0 = st.number_input("Null Hypothesis Value (μ₀)", value=10.0)
        alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05)
    
    with col2:
        alt = st.selectbox("Alternative Hypothesis", ["two-sided", "greater", "less"])

    # Process data
    try:
        data_list = [float(x.strip()) for x in raw_data.split(",")]
        
        if st.button("Run T-Test"):
            results = ttest(data_list, mu0, alpha, alt)
            st.session_state['test_results'] = results
            st.success("Test completed! Check the Results tab.")
    except ValueError:
        st.error("Please enter valid numbers separated by commas.")

with tab2:
    if 'test_results' in st.session_state:
        res = st.session_state['test_results']
        
        st.subheader("Test Summary")
        
        # Displaying metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Sample Mean (x̄)", round(res['xbar'], 3))
        m2.metric("T-Calculated", round(res['t_cal'], 3))
        m3.metric("P-Value", round(res['p_value'], 4))
        
        # Result Highlight
        if "Reject" in res['decision']:
            st.error(f"**Decision:** {res['decision']}")
        else:
            st.success(f"**Decision:** {res['decision']}")
            
        with st.expander("View Full Details"):
            st.json(res)
    else:
        st.info("Run the test in the 'Input Data' tab to see results here.")