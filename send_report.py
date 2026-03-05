"""
send_report.py
Sends Robot Framework HTML report via Gmail after test run.
Reads credentials from environment variables (GitHub Actions Secrets).
"""

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# ─── CONFIG — reads from GitHub Secrets (env vars) ────────────────────────────
SENDER_EMAIL      = os.environ.get("SENDER_EMAIL",    "kottunagaraju.4354@gmail.com")
SENDER_PASSWORD   = os.environ.get("SENDER_PASSWORD", "groo jxex csps qmf")
RECIPIENT_EMAIL   = os.environ.get("RECIPIENT_EMAIL", "kottunagaraju.4354@gmail.com")
RESULTS_DIR       = os.environ.get("RESULTS_DIR",     "results")
# ──────────────────────────────────────────────────────────────────────────────


def get_test_summary():
    output_xml = os.path.join(RESULTS_DIR, "output.xml")
    passed, failed, total = 0, 0, 0
    status = "UNKNOWN"
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(output_xml)
        root = tree.getroot()
        for stat in root.iter("stat"):
            if stat.get("name") == "All Tests":
                passed = int(stat.get("pass", 0))
                failed = int(stat.get("fail", 0))
                total  = passed + failed
                status = "PASSED" if failed == 0 else "FAILED"
                break
    except FileNotFoundError:
        status = "NO RESULTS"
    except Exception as e:
        status = f"ERROR: {e}"
    return passed, failed, total, status


def build_email_body(passed, failed, total, status):
    run_time = datetime.now().strftime("%d-%b-%Y %I:%M %p IST")
    color    = "#28a745" if status == "PASSED" else "#dc3545"
    emoji    = "✅" if status == "PASSED" else "❌"
    return f"""
    <html>
    <body style="font-family:Arial,sans-serif;padding:20px;background:#f9f9f9;">
      <div style="max-width:500px;background:white;padding:24px;border-radius:8px;
                  border-left:5px solid {color};box-shadow:0 2px 8px rgba(0,0,0,0.1);">
        <h2 style="color:{color};margin-top:0;">🤖 Naukri Automation — Daily Report</h2>
        <table border="1" cellpadding="10" cellspacing="0"
               style="border-collapse:collapse;width:100%;font-size:14px;">
          <tr style="background:#f2f2f2;"><th align="left">Metric</th><th align="left">Value</th></tr>
          <tr><td>📅 Run Date &amp; Time</td><td>{run_time}</td></tr>
          <tr><td>📋 Total Tests</td><td>{total}</td></tr>
          <tr><td style="color:#28a745;">✅ Passed</td><td><b>{passed}</b></td></tr>
          <tr><td style="color:#dc3545;">❌ Failed</td><td><b>{failed}</b></td></tr>
          <tr><td><b>Overall Status</b></td>
              <td style="color:{color};font-weight:bold;font-size:16px;">{emoji} {status}</td></tr>
        </table>
        <br>
        <p>📎 Full HTML report attached — open <b>report.html</b> in your browser.</p>
        <hr style="border:none;border-top:1px solid #eee;">
        <p style="color:grey;font-size:11px;">🕛 Scheduled: Daily at 12:00 AM IST &nbsp;|&nbsp; Powered by GitHub Actions</p>
      </div>
    </body></html>
    """


def send_email():
    passed, failed, total, status = get_test_summary()
    run_date = datetime.now().strftime("%d-%b-%Y")
    emoji    = "✅" if status == "PASSED" else "❌"

    msg            = MIMEMultipart("alternative")
    msg["Subject"] = f"[Naukri Automation] Daily Report {run_date} — {emoji} {status}"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECIPIENT_EMAIL

    msg.attach(MIMEText(build_email_body(passed, failed, total, status), "html"))

    report_path = os.path.join(RESULTS_DIR, "report.html")
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="naukri_report_{run_date}.html"')
            msg.attach(part)
        print(f"📎 Report attached")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print(f"✅ Email sent to {RECIPIENT_EMAIL} | {emoji} {status} | P:{passed} F:{failed}")
    except Exception as e:
        print(f"❌ Email failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    send_email()
