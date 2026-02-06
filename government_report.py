from datetime import datetime

def generate_report(risk_score, status, reasons):
    report = f"""
AI EARLY DISEASE WARNING REPORT
------------------------------
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Village: Sample Village

Risk Score: {risk_score}
Status: {status}

Reasons:
{reasons}

Recommended Action:
- Increase medical stock
- Deploy health workers
- Issue public advisory
"""
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(f"reports/{filename}", "w") as f:
        f.write(report)

    return filename
