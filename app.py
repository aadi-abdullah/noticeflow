"""
NoticeFlow Lite – Streamlit UI
A lightweight tax notice triage tool for Pakistani chartered accountants.

This module implements the web interface for uploading tax notices and
displaying structured extraction results.

Usage:
    streamlit run app.py
"""

import streamlit as st
from datetime import datetime, timedelta
import json
from process_notice import process_notice

# Page configuration
st.set_page_config(
    page_title="NoticeFlow Lite",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling and mobile responsiveness
st.markdown("""
    <style>
    /* Main container padding */
    .main {
        padding: 1rem;
    }
    
    /* Deadline styling - color coded */
    .deadline-urgent {
        font-size: 2.5em;
        font-weight: bold;
        color: #d32f2f;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        background-color: #ffebee;
        margin: 1rem 0;
    }
    
    .deadline-warning {
        font-size: 2.5em;
        font-weight: bold;
        color: #f57c00;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        background-color: #fff3e0;
        margin: 1rem 0;
    }
    
    .deadline-safe {
        font-size: 2.5em;
        font-weight: bold;
        color: #388e3c;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        background-color: #e8f5e9;
        margin: 1rem 0;
    }
    
    /* Risk level styling */
    .risk-high {
        border-left: 4px solid #d32f2f;
        padding: 0.5rem 1rem;
        background-color: #ffebee;
        border-radius: 4px;
    }
    
    .risk-medium {
        border-left: 4px solid #f57c00;
        padding: 0.5rem 1rem;
        background-color: #fff3e0;
        border-radius: 4px;
    }
    
    .risk-low {
        border-left: 4px solid #388e3c;
        padding: 0.5rem 1rem;
        background-color: #e8f5e9;
        border-radius: 4px;
    }
    
    /* Checklist styling */
    .checklist-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background-color: #f5f5f5;
        border-radius: 4px;
        border-left: 3px solid #2196F3;
    }
    
    /* Disclaimer footer */
    .disclaimer {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #fafafa;
        border-left: 4px solid #757575;
        border-radius: 4px;
        font-size: 0.85em;
        color: #666;
        text-align: center;
    }
    
    /* Uncertainty warning */
    .uncertainty-box {
        background-color: #fff9c4;
        border-left: 4px solid #f57f17;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Header styling */
    .main-title {
        text-align: center;
        color: #1a237e;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.95em;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def get_urgency_level(deadline_str):
    """
    Determine urgency level based on days remaining until deadline.
    
    Args:
        deadline_str (str): Deadline date in YYYY-MM-DD format or None.
    
    Returns:
        tuple: (urgency_level, days_remaining, color_class)
        - urgency_level (str): 'high', 'medium', or 'low'
        - days_remaining (int): Number of days until deadline (negative if overdue)
        - color_class (str): CSS class name for styling
    """
    if not deadline_str:
        return None, None, None
    
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        today = datetime.now()
        days_remaining = (deadline - today).days
        
        if days_remaining < 0:
            return 'high', days_remaining, 'deadline-urgent'
        elif days_remaining < 7:
            return 'high', days_remaining, 'deadline-urgent'
        elif days_remaining < 14:
            return 'medium', days_remaining, 'deadline-warning'
        else:
            return 'low', days_remaining, 'deadline-safe'
    except ValueError:
        return None, None, None


def display_deadline(deadline_str, days_remaining, color_class):
    """
    Display the deadline with color-coded urgency indicator.
    
    Args:
        deadline_str (str): Deadline date in YYYY-MM-DD format.
        days_remaining (int): Number of days until deadline.
        color_class (str): CSS class for styling.
    """
    if color_class == 'deadline-urgent':
        icon = "🚨"
        urgency_text = "URGENT"
    elif color_class == 'deadline-warning':
        icon = "⚠️"
        urgency_text = "ATTENTION"
    else:
        icon = "✅"
        urgency_text = "SAFE"
    
    deadline_display = f"{deadline_str} ({days_remaining} days remaining)"
    st.markdown(
        f'<div class="{color_class}">{icon} {deadline_display}<br/><small>{urgency_text}</small></div>',
        unsafe_allow_html=True
    )


def display_uncertainty_warnings(uncertainties):
    """
    Display warnings for any fields with low confidence or missing data.
    
    Args:
        uncertainties (list): List of uncertainty strings in format "field: reason".
    """
    if uncertainties and len(uncertainties) > 0:
        st.markdown(
            '<div class="uncertainty-box">',
            unsafe_allow_html=True
        )
        st.warning(f"⚠️ **Data Quality Notice**: The system is uncertain about {len(uncertainties)} field(s). Please verify:")
        for uncertainty in uncertainties:
            st.markdown(f"- {uncertainty}")
        st.markdown('</div>', unsafe_allow_html=True)


def display_results(result):
    """
    Display extraction results in a user-friendly format.
    
    Args:
        result (dict): Result dictionary from process_notice().
    """
    # Check for errors
    if "error" in result:
        st.error(f"⚠️ Processing failed: {result['error']}")
        return
    
    # Extract data with safe defaults
    deadline = result.get("deadline")
    section = result.get("section_cited", "Unknown")
    tax_year = result.get("tax_year", "Unknown")
    allegations = result.get("allegations_summary", [])
    checklist = result.get("document_checklist", [])
    risk_level = result.get("risk_level", "unknown").lower()
    risk_reason = result.get("risk_reason", "Unable to assess risk")
    uncertainties = result.get("uncertainties", [])
    
    # === DEADLINE SECTION ===
    st.markdown("---")
    st.markdown("### 📅 Deadline")
    
    if deadline:
        urgency, days, color_class = get_urgency_level(deadline)
        if urgency:
            display_deadline(deadline, days, color_class)
        else:
            st.info(f"📅 Deadline: {deadline}")
    else:
        st.warning("❌ Deadline not found in notice. Please verify manually.")
    
    # === SECTION & TAX YEAR ===
    st.markdown("---")
    st.markdown("### 📋 Notice Details")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tax Section", value=section)
    with col2:
        st.metric(label="Tax Year", value=tax_year)
    
    # === ALLEGATIONS/SUMMARY ===
    st.markdown("---")
    st.markdown("### 📝 What FBR Says")
    if allegations:
        for allegation in allegations:
            st.markdown(f"- {allegation}")
    else:
        st.info("No specific allegations extracted. Review the original notice for details.")
    
    # === RISK LEVEL ===
    st.markdown("---")
    st.markdown("### ⚖️ Risk Assessment")
    
    risk_color_map = {
        "high": "risk-high",
        "medium": "risk-medium",
        "low": "risk-low"
    }
    risk_color = risk_color_map.get(risk_level, "risk-medium")
    risk_emoji_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    risk_emoji = risk_emoji_map.get(risk_level, "⚪")
    
    st.markdown(
        f'<div class="{risk_color}"><strong>{risk_emoji} Risk Level: {risk_level.upper()}</strong><br/>{risk_reason}</div>',
        unsafe_allow_html=True
    )
    
    # === DOCUMENT CHECKLIST ===
    st.markdown("---")
    st.markdown("### ✅ Required Documents")
    if checklist:
        for idx, item in enumerate(checklist, 1):
            st.markdown(f'<div class="checklist-item">☐ {item}</div>', unsafe_allow_html=True)
    else:
        st.info("No specific documents extracted. Refer to FBR guidelines for your section.")
    
    # === UNCERTAINTY WARNINGS ===
    if uncertainties:
        st.markdown("---")
        display_uncertainty_warnings(uncertainties)
    
    # === DISCLAIMER ===
    st.markdown("---")
    st.markdown(
        """
        <div class="disclaimer">
        <strong>⚠️ Important Disclaimer</strong><br/>
        This tool provides extraction assistance only. Always verify all extracted information against the original notice. 
        Final decisions regarding notice interpretation, document collection, and response strategy remain the 
        professional's responsibility. NoticeFlow Lite does not provide legal or tax advice.
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """
    Main Streamlit application logic.
    Handles file upload, processing, and result display.
    """
    # Header
    st.markdown('<h1 class="main-title">📋 NoticeFlow Lite</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Instant FBR Notice Triage for Pakistani CAs</p>',
        unsafe_allow_html=True
    )
    st.markdown('<p class="subtitle" style="font-size: 0.85em; color: #999;">Upload a tax notice and instantly get deadlines, explanations, and document checklists.</p>', 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        label="📤 Upload Tax Notice",
        type=["pdf", "png", "jpg", "jpeg"],
        help="PDF or image (JPG/PNG) of your FBR/IRIS notice. Supports scanned documents and photos."
    )
    
    if uploaded_file is not None:
        # Show file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        # Processing
        with st.spinner("🔄 Processing notice... (typically 10-20 seconds)"):
            result = process_notice(uploaded_file)
        
        # Display results
        display_results(result)


if __name__ == "__main__":
    main()
