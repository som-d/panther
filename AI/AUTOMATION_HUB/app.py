#!/usr/bin/env python3
"""
SOHAM'S PLACEMENT AUTOMATION HUB
Your Personal Career Command Center

Usage:
    python app.py                  -> Show interactive menu
    python app.py dashboard        -> Show stats
    python app.py blast            -> Send emails to all contacts
    python app.py launch-jobs      -> Open all active jobs in browser
    python app.py track            -> Update application status
    python app.py linkedin         -> LinkedIn helper
    python app.py report           -> Generate weekly report
    python app.py learn            -> Open learning resources
    python app.py setup            -> First-time configuration
    python app.py followup         -> Send follow-up emails
    python app.py check-tasks      -> Show today's tasks
    python app.py analyze          -> Analyze a company (jobs + contacts + ATS)
    python app.py agent <company>  -> Unified AI agent for jobs+recruiters outreach
    python app.py blast            -> AI-powered email blast (dynamic generation)
"""

import sys
import io
# Force UTF-8 output for Windows console compatibility
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import csv
import os
import webbrowser
import smtplib
import ssl
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# --- CONSTANTS ---
BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ASCII symbols for cross-platform compatibility
CHECK = "[OK]"
CROSS = "[XX]"
ARROW = " -> "
WARN = "[!!]"
STAR = "[*]"
DASH = "-"
PENDING = "[ ]"
DONE = "[X]"


def load_config():
    if not CONFIG_PATH.exists():
        print(f" {CROSS} config.json not found! Run: python app.py setup")
        sys.exit(1)
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f" {CHECK} Config saved!")


def load_csv(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_csv(filepath, data, fieldnames):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def init_applications_csv():
    path = DATA_DIR / "applications.csv"
    if not path.exists():
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Company", "Job_Title", "Apply_Link", "Salary",
                             "Status", "Contact_Name", "Contact_Email", "Notes"])
        print(f" {CHECK} Created applications tracking file")


def init_email_log_csv():
    path = DATA_DIR / "email_log.csv"
    if not path.exists():
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "To", "Company", "Subject", "Template",
                             "Status", "Followed_Up", "Reply_Received"])
        print(f" {CHECK} Created email log file")


# ===================== DASHBOARD =====================

def show_dashboard():
    config = load_config()
    init_applications_csv()
    init_email_log_csv()

    jobs = load_csv(DATA_DIR / "Active_Job_Listings.csv")
    contacts = load_csv(DATA_DIR / "Email_Contact_List.csv")
    applications = load_csv(DATA_DIR / "applications.csv")
    email_log = load_csv(DATA_DIR / "email_log.csv")

    total_apps = len(applications) if applications else 0
    applied = sum(1 for a in applications if a.get('Status') == 'Applied') if applications else 0
    interviewing = sum(1 for a in applications if 'Interview' in a.get('Status', '')) if applications else 0
    offers = sum(1 for a in applications if a.get('Status') == 'Offer') if applications else 0
    rejected = sum(1 for a in applications if a.get('Status') == 'Rejected') if applications else 0
    emails_sent = len(email_log) if email_log else 0

    def safe_match(j):
        ms = j.get('Match_Score', '0').replace('%', '')
        return ms.isdigit() and int(ms) >= 60

    active_jobs = len([j for j in jobs if safe_match(j)]) if jobs else 0

    def safe_priority(c):
        p = c.get('Priority', '')
        return p.startswith('1') if p else False

    high_priority = len([c for c in contacts if safe_priority(c)]) if contacts else 0

    email_setup = config.get('gmail', {}).get('app_password', '') != 'YOUR_16_CHAR_APP_PASSWORD_HERE'
    k8s_started = config.get('learning_track', {}).get('started_k8s', False)

    LINE = "=" * 55
    print(f"\n{LINE}")
    print(f"  YOUR PLACEMENT DASHBOARD")
    print(LINE)
    print(f"  Target:       {config['personal']['target_role']}")
    print(f"  Location:     {config['preferences']['job_search_location']}")
    sal_min = config['preferences']['salary_expectation_min'] // 100000
    sal_max = config['preferences']['salary_expectation_max'] // 100000
    print(f"  Salary:       INR {sal_min}-{sal_max} LPA")
    print("-" * 55)
    print(f"  Jobs Found:          {len(jobs)}")
    print(f"  Best-Fit (60%+):     {active_jobs}")
    print(f"  Contacts:            {len(contacts)}")
    print(f"  High Priority:       {high_priority}")
    print("-" * 55)
    print(f"  Applications Total:  {total_apps}")
    print(f"  Applied:             {applied}")
    print(f"  Interviewing:        {interviewing}")
    print(f"  Offers:              {offers}")
    print(f"  Rejected:            {rejected}")
    print("-" * 55)
    print(f"  Emails Sent:         {emails_sent}")
    print(f"  Email Auto:          {'YES' if email_setup else 'NO - run setup'}")
    print(f"  K8s Learning:        {'YES' if k8s_started else 'Not yet'}")
    print("-" * 55)

    if applications:
        resp = interviewing + offers
        rate = (resp / len(applications)) * 100
        print(f"  Response Rate:       {rate:.1f}% ({resp}/{len(applications)})")
    print(LINE)

    print(f"\n  NEXT SUGGESTED ACTION:")
    if not email_setup:
        print(f"     {WARN} Run 'python app.py setup' - Email NOT configured!")
    elif total_apps == 0:
        print(f"     Run 'python app.py launch-jobs' to start applying!")
    elif emails_sent == 0:
        print(f"     Run 'python app.py blast' to send your first emails!")
    elif not k8s_started:
        print(f"     Run 'python app.py learn' to start Kubernetes!")
    elif interviewing == 0 and total_apps >= 20:
        print(f"     Waiting for responses... Increase applications!")
    elif interviewing > 0 and offers == 0:
        print(f"     You have interviews! Prep with STAR stories.")
    elif offers > 0:
        print(f"     YOU HAVE OFFERS! Negotiate and close!")
    else:
        print(f"     Keep going! Check: python app.py check-tasks")
    print()


# ===================== EMAIL =====================

def send_email(config, to_email, subject, body_html, contact_name="", company=""):
    username = config['gmail']['username']
    password = config['gmail']['app_password']

    if password == "YOUR_16_CHAR_APP_PASSWORD_HERE":
        print(f"  Skipping {to_email} - App password not set! Run 'python app.py setup'")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject

        text_plain = body_html.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n').replace('<li>', '- ').replace('</li>', '').replace('<ul>', '').replace('</ul>', '').replace('<strong>', '').replace('</strong>', '').replace('<a href=', '').replace('</a>', '').replace('>', ' ')
        msg.attach(MIMEText(text_plain, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))

        resume_path = config['system']['resume_path']
        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                att = MIMEBase('application', 'octet-stream')
                att.set_payload(f.read())
                encoders.encode_base64(att)
                att.add_header('Content-Disposition', 'attachment', filename='Soham_Deshmukh_DevOps_Engineer.pdf')
                msg.attach(att)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(username, password)
            server.send_message(msg)

        log_email(config, to_email, company, subject, "Sent")
        print(f"  {CHECK} Sent to {contact_name or to_email} ({company})")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"  {CROSS} Gmail auth failed! Check app password.")
        print(f"     Get it: https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"  {CROSS} Failed to send to {to_email}: {str(e)[:100]}")
        log_email(config, to_email, company, subject, f"Failed: {str(e)[:50]}")
        return False


def log_email(config, to_email, company, subject, status):
    path = DATA_DIR / "email_log.csv"
    fieldnames = ["Date", "To", "Company", "Subject", "Template", "Status", "Followed_Up", "Reply_Received"]

    existing = []
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            existing = list(csv.DictReader(f))

    existing.append({
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "To": to_email,
        "Company": company,
        "Subject": subject,
        "Template": "Custom",
        "Status": status,
        "Followed_Up": "No",
        "Reply_Received": ""
    })

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)


def email_blaster(config=None):
    if config is None:
        config = load_config()

    from intelligence import AIEmailGenerator, EmailValidator, SpamChecker, SendOptimizer

    ai = AIEmailGenerator(config.get('ai', {}).get('gemini_api_key'))
    validator = EmailValidator()
    spam_checker = SpamChecker()
    optimizer = SendOptimizer()

    contacts = load_csv(DATA_DIR / "Email_Contact_List.csv")
    jobs = load_csv(DATA_DIR / "Active_Job_Listings.csv")
    init_email_log_csv()

    if not contacts:
        print(f" {CROSS} No contacts found in Email_Contact_List.csv")
        return

    def priority_sort(c):
        p = c.get('Priority', '3')
        return int(p[0]) if p and p[0].isdigit() else 3

    contacts.sort(key=priority_sort)

    # Load previously sent emails to avoid duplicates
    already_sent = set()
    try:
        sent_log = load_csv(DATA_DIR / "email_log.csv")
        for entry in sent_log:
            addr = entry.get('To', '').strip().lower()
            if addr:
                already_sent.add(addr)
    except:
        pass

    # Build company -> job mapping
    company_jobs = {}
    for j in jobs:
        c = j.get('Company', '').lower()
        if c not in company_jobs:
            company_jobs[c] = []
        company_jobs[c].append(j)

    # --- PREVIEW PASS ---
    to_send = []
    for i, contact in enumerate(contacts, 1):
        name = contact.get('Contact Name', 'Hiring Manager')
        company = contact.get('Company', 'Company')
        email = contact.get('Email', '').strip().lower()
        priority = contact.get('Priority', '3')

        if not email or 'pattern' in email.lower():
            continue

        email_conf = contact.get('Email_Confidence', '')

        # Skip if already sent to this email
        if email in already_sent:
            print(f"  Skip {name} @ {company} - already sent previously")
            continue

        skip = not ('CONFIRMED' in email_conf or 'HIGH' in email_conf)
        if skip and len(to_send) >= 5:
            continue

        to_send.append((i, name, company, email, email_conf, priority, contact.get('Notes', '')))

    if not to_send:
        print(f" {CROSS} No contacts with confirmed emails to send to")
        return

    # Pre-generate all AI content
    print(f"\n Preparing AI-generated emails... (may take a moment)")
    print("=" * 55)

    email_contents = []
    for idx, (i, name, company, email, conf, pri, notes) in enumerate(to_send, 1):
        first_name = name.split()[0] if ' ' in name else name

        # Find matching job for this company - pick highest match score
        matching_jobs = company_jobs.get(company.lower(), [])
        role_title = 'DevOps Engineer'
        job_highlights = ''
        if matching_jobs:
            best_job = matching_jobs[0]
            best_score = 0
            for j in matching_jobs:
                ms = j.get('Match_Score', '0').replace('%', '')
                if ms.isdigit() and int(ms) > best_score:
                    best_score = int(ms)
                    best_job = j
            role_title = best_job.get('Job_Title', 'DevOps Engineer')
            job_highlights = best_job.get('Notes', '')

        # Generate subject dynamically
        subject = ai.generate_subject(company, role_title, name)

        # Generate email body dynamically using AI
        body = ai.generate_email(name, company, role_title, notes, job_highlights)

        # Wrap in HTML
        body_html = f"""<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
{body.replace('\n\n', '</p><p>').replace('\n', '<br>') if body else ''}
</body></html>"""

        email_contents.append({
            'name': name, 'company': company, 'email': email,
            'subject': subject, 'body': body_html, 'plain_body': body,
            'role_title': role_title, 'notes': notes
        })

    # --- PREVIEW ---
    print(f"\nEMAIL BLASTER - AI POWERED PREVIEW")
    print("=" * 55)
    print(f"AI Status: {'GEMINI ACTIVE' if ai.available else 'FALLBACK MODE (no API key)'}")
    print(f"Recipients: {len(email_contents)}")
    print("-" * 55)

    for idx, ec in enumerate(email_contents, 1):
        # Validate email
        val_result = validator.validate(ec['email'])
        val_icon = CHECK if val_result['valid'] else CROSS

        print(f"\n=== EMAIL {idx}: {ec['name']} @ {ec['company']} ===")
        print(f"  TO:       {ec['email']}  {val_icon}")
        if not val_result['valid']:
            for issue in val_result['issues']:
                print(f"            WARNING: {issue}")
        print(f"  SUBJECT:  {ec['subject']}")
        print(f"  CONTENT:")
        for line in ec['plain_body'].strip().split('\n')[:8]:
            print(f"    {line.strip()}")
        if len(ec['plain_body'].split('\n')) > 8:
            print(f"    ...")
        print("-" * 40)

    # Critical checks summary
    print(f"\n  CRITICAL CHECKS:")
    checks_passed = 0
    checks_total = 4

    # Check 1: Timing
    timing = optimizer.best_time_to_send()
    if timing['should_send']:
        print(f"    {CHECK} Timing: {timing['reason']}")
        checks_passed += 1
    else:
        print(f"    {WARN} Timing: {timing['reason']}")
        if timing.get('suggested_time'):
            print(f"         Best to send: {timing['suggested_time']}")

    # Check 2: Spam score
    for ec in email_contents:
        spam_result = spam_checker.check_spam_score(ec['body'])
        if spam_result['grade'] == 'FAIL':
            print(f"    {CROSS} SPAM RISK: {ec['name']}'s email scores {spam_result['spam_score']}%")
            for issue in spam_result['issues']:
                print(f"         {issue}")
            break
    else:
        print(f"    {CHECK} Spam check: All emails pass")
        checks_passed += 1

    # Check 3: All emails validated
    all_valid = all(validator.validate(ec['email'])['valid'] for ec in email_contents)
    if all_valid:
        print(f"    {CHECK} Email validation: All addresses valid")
        checks_passed += 1
    else:
        print(f"    {WARN} Email validation: Some addresses have issues")

    # Check 4: Application consistency
    apps = load_csv(DATA_DIR / "applications.csv")
    for ec in email_contents:
        company_apps = [a for a in apps if a.get('Company', '').lower() == ec['company'].lower()]
        if company_apps:
            print(f"    {CHECK} Application found: {ec['company']} - {company_apps[0].get('Job_Title', '')}")
            checks_passed += 1
        else:
            print(f"    {WARN} No application logged for {ec['company']} - send career portal link instead")
        break  # Just check the first one

    print(f"\n  CHECKS PASSED: {checks_passed}/{checks_total}")

    # --- ASK FOR APPROVAL ---
    print(f"\nSend {len(email_contents)} AI-personalized email(s) now?")
    choice = input("  Type 'yes' to send, anything else to cancel: ").strip().lower()

    if choice != 'yes':
        print(f" {CROSS} Email blast cancelled. No emails sent.")
        return

    # --- SEND PASS ---
    print(f"\nEMAIL BLASTER - SENDING")
    print("-" * 50)

    for idx, ec in enumerate(email_contents, 1):
        print(f"  {idx}. Sending to {ec['name']:25s} @ {ec['company']:20s} ({ec['email']})")
        send_email(config, ec['email'], ec['subject'], ec['body'], ec['name'], ec['company'])

    print("-" * 50)
    print(f" {CHECK} Email blast complete! (AI-generated, dynamic content)")
    print("   Check email_log.csv for status.\n")


def send_follow_ups(config):
    log = load_csv(DATA_DIR / "email_log.csv")
    if not log:
        print(f" {CROSS} No emails sent yet to follow up on")
        return

    days_wait = config['preferences']['follow_up_days']
    cutoff = datetime.now() - timedelta(days=days_wait)

    to_follow = []
    for entry in log:
        if entry.get('Status') == 'Sent' and entry.get('Followed_Up') == 'No':
            try:
                sent_date = datetime.strptime(entry['Date'].split()[0], "%Y-%m-%d")
                if sent_date < cutoff:
                    to_follow.append(entry)
            except:
                pass

    if not to_follow:
        print(f" {CHECK} No pending follow-ups (need {days_wait}d since last email)")
        return

    print(f"\nFOLLOW-UP PREVIEW - {len(to_follow)} email(s) ready for follow-up")
    print("-" * 50)
    for i, entry in enumerate(to_follow, 1):
        sent_d = entry.get('Date', 'unknown').split()[0]
        print(f"  {i}. To: {entry['To']:35s} | Company: {entry['Company']:20s} | Sent: {sent_d}")
    print("-" * 50)
    print("\nSample follow-up message:")
    print("  Subject: Re: DevOps Engineer | Following up")
    print("  Hi there,")
    print("  Following up on my previous note about DevOps opportunities.")
    print("  Would you have 5 minutes to connect this week?")
    print()

    choice = input("Send these follow-ups now? (type 'yes' to send): ").strip().lower()
    if choice != 'yes':
        print(f" {CROSS} Follow-ups cancelled.")
        return

    print(f"\nFOLLOW-UP BLASTER - SENDING")
    for entry in to_follow:
        subject = f"Re: DevOps Engineer | Following up"
        body = f"""<html><body style="font-family: Arial, sans-serif;">
<p>Hi there,</p>
<p>Following up on my previous note about DevOps opportunities at <strong>{entry['Company']}</strong>.</p>
<p>I wanted to circle back in case my earlier message got buried. I'm highly interested in contributing to your team.</p>
<p>Would you have 5 minutes to connect this week?</p>
<p>Best,<br><strong>Soham Deshmukh</strong></p>
</body></html>"""
        print(f"  -> Sending to {entry['To']} ({entry['Company']})")
        send_email(config, entry['To'], subject, body, entry['To'], entry['Company'])

    print(f" {CHECK} Follow-ups sent!")


# ===================== JOB LAUNCHER =====================

def launch_jobs(config=None):
    if config is None:
        config = load_config()

    jobs = load_csv(DATA_DIR / "Active_Job_Listings.csv")
    init_applications_csv()

    if not jobs:
        print(f" {CROSS} No job listings found in Active_Job_Listings.csv")
        return

    print(f"\nJOB LAUNCHER - Opening {len(jobs)} jobs in browser")
    print("-" * 55)

    for i, job in enumerate(jobs, 1):
        company = job.get('Company', 'Company')
        title = job.get('Job_Title', 'Role')
        match = job.get('Match_Score', '')
        link = job.get('Apply_Link', '')

        if link and link.startswith('http'):
            print(f"  {i:2d}. [{match:>3}] {company} - {title[:40]}")
            webbrowser.open_new_tab(link)
        else:
            print(f"  {i:2d}. Skip  {company} - {title[:40]} (no link)")

    print("-" * 55)
    print(f" {CHECK} {len(jobs)} job pages opened in browser tabs!")
    print("   Now manually apply to each one.")
    print("   After applying, run: python app.py track\n")


# ===================== APPLICATION TRACKER =====================

def track_application(config=None):
    if config is None:
        config = load_config()

    init_applications_csv()
    apps = load_csv(DATA_DIR / "applications.csv")

    print("\nAPPLICATION TRACKER")
    print("=" * 55)
    print("  1. Log a NEW application")
    print("  2. Update existing application status")
    print("  3. View all applications")
    print("  4. Back to main menu")
    print("-" * 55)

    choice = input("  Choose (1-4): ").strip()

    if choice == '1':
        print("\n  Log New Application:")
        date = datetime.now().strftime("%Y-%m-%d")
        company = input("  Company: ").strip()
        title = input("  Job Title: ").strip()
        link = input("  Apply Link (optional): ").strip()
        salary = input("  Salary (optional): ").strip()

        apps.append({
            "Date": date, "Company": company, "Job_Title": title,
            "Apply_Link": link, "Salary": salary, "Status": "Applied",
            "Contact_Name": "", "Contact_Email": "", "Notes": ""
        })

        save_csv(DATA_DIR / "applications.csv", apps,
                 ["Date", "Company", "Job_Title", "Apply_Link", "Salary",
                  "Status", "Contact_Name", "Contact_Email", "Notes"])
        print(f"  {CHECK} Logged: {company} - {title}")

    elif choice == '2':
        if not apps:
            print("  No applications to update")
            return

        print("\n  Your Applications:")
        for i, app in enumerate(apps, 1):
            icons = {"Applied": "[A]", "Interview Scheduled": "[I]",
                     "Interview Done": "[DONE]", "Offer": "[OFFER]",
                     "Rejected": "[NO]", "No Reply": "[...]"}
            icon = icons.get(app.get('Status', ''), "[?]")
            print(f"  {i:2d}. {icon} {app['Company']} - {app['Job_Title'][:30]} [{app['Status']}]")

        idx = input("\n  Enter number to update: ").strip()
        if idx.isdigit() and 1 <= int(idx) <= len(apps):
            i = int(idx) - 1
            print(f"\n  Current: {apps[i]['Company']} - {apps[i]['Job_Title']}")
            print("  New Status:")
            print("    1. Applied (initial)")
            print("    2. Interview Scheduled")
            print("    3. Interview Done")
            print("    4. Offer")
            print("    5. Rejected")
            print("    6. No Reply")

            status_map = {'1': 'Applied', '2': 'Interview Scheduled', '3': 'Interview Done',
                         '4': 'Offer', '5': 'Rejected', '6': 'No Reply'}
            s = input("  Choose (1-6): ").strip()
            if s in status_map:
                apps[i]['Status'] = status_map[s]
                notes = input("  Notes (optional): ").strip()
                if notes:
                    apps[i]['Notes'] = notes
                save_csv(DATA_DIR / "applications.csv", apps,
                        ["Date", "Company", "Job_Title", "Apply_Link", "Salary",
                         "Status", "Contact_Name", "Contact_Email", "Notes"])
                print(f"  {CHECK} Updated: {apps[i]['Company']} -> {status_map[s]}")

    elif choice == '3':
        if not apps:
            print("  No applications yet")
            return
        print(f"\n  ALL APPLICATIONS ({len(apps)} total):")
        print("-" * 55)
        for i, app in enumerate(apps, 1):
            icons = {"Applied": "[A]", "Interview Scheduled": "[I]",
                     "Interview Done": "[DONE]", "Offer": "[OFFER]",
                     "Rejected": "[NO]", "No Reply": "[...]"}
            icon = icons.get(app.get('Status', ''), "[?]")
            print(f"  {i:2d}. {icon} {app['Company']:20s} | {app['Job_Title'][:25]:25s} | {app['Status']:20s} | {app['Date']}")
        print("-" * 55)

    input("\n  Press Enter to continue...")


# ===================== LINKEDIN HELPER =====================

def linkedin_helper(config=None):
    if config is None:
        config = load_config()

    print("\nLINKEDIN HELPER")
    print("=" * 55)
    print("  1. Open Profile (for editing headline/about)")
    print("  2. Open 'Start a Post' (to publish draft posts)")
    print("  3. Open Job Search 'DevOps Engineer Pune'")
    print("  4. Open Connection Search (find recruiters)")
    print("  5. View suggested posts to publish")
    print("  6. Back")
    print("-" * 55)

    choice = input("  Choose (1-6): ").strip()

    if choice == '1':
        webbrowser.open_new_tab("https://www.linkedin.com/in/soham-deshmukh-142939225/edit/intro")
        print("  Profile edit page opened!")
        print("\n  SET YOUR HEADLINE TO:")
        print("  +-------------------------------------------------------+")
        print("  | DevOps Engineer | Ansible | Terraform | Azure | CI/CD  |")
        print("  +-------------------------------------------------------+")

    elif choice == '2':
        webbrowser.open_new_tab("https://www.linkedin.com/feed/?linkOrigin=LI_COMMERCE_FEED&startPost=true")
        print("  LinkedIn post composer opened!")
        print("\n  POST IDEAS (copy from MASTER_PLAN.md):")
        posts = [
            "Post 1: How I reduced incident response by 40%",
            "Post 2: Terraform + Ansible = Azure Superpower",
            "Post 3: Your CI/CD pipeline is missing this",
            "Post 4: LLMs + DevOps - My Experiment",
        ]
        for p in posts:
            print(f"     * {p}")

    elif choice == '3':
        webbrowser.open_new_tab("https://www.linkedin.com/jobs/search/?keywords=DevOps%20Engineer&location=Pune%2C%20India")
        print("  LinkedIn job search opened!")

    elif choice == '4':
        webbrowser.open_new_tab("https://www.linkedin.com/search/results/people/?keywords=Talent%20Acquisition%20Pune%20DevOps")
        print("  Recruiter search opened! Connect with 10 people.")

    elif choice == '5':
        print("\n  DRAFT POSTS READY TO PUBLISH:")
        print("-" * 55)
        print("  POST 1 (Technical):")
        print()
        print("  How I built an auto-remediation platform that cut")
        print("  incident handling by 40%")
        print()
        print("  At Wipro, I built an event-driven automation pipeline:")
        print("  LogicMonitor -> BigPanda -> Jenkins + Docker -> ServiceNow -> Ansible AAP")
        print()
        print("  Result: ~40% reduction in manual incident handling.")
        print()
        print("  #DevOps #Automation #Ansible #Azure #SRE")
        print("-" * 55)
        print("  More posts in LinkedIn_Review_And_Setup_Guide.md")

    input("\n  Press Enter to continue...")


# ===================== LEARNING CENTER =====================

def open_learning(config=None):
    if config is None:
        config = load_config()

    print("\nLEARNING CENTER")
    print("=" * 55)
    print("  KUBERNETES LEARNING PATH (15 min/day)")
    print("-" * 55)
    print("  Week 1: Pods & Deployments (K8s for Beginners)")
    print("  Week 2: Services & Networking")
    print("  Week 3: Helm & ConfigMaps")
    print("  Week 4: AKS on Azure (hands-on)")
    print("  Week 5: Prometheus/Grafana on K8s")
    print("  Week 6: CI/CD on K8s with GitHub Actions")
    print("-" * 55)

    print("\n  Open learning resource:")
    print("  1. KodeKloud - Kubernetes for Beginners (FREE)")
    print("  2. Kubernetes Official Tutorials")
    print("  3. Azure AKS Quickstart")
    print("  4. All of the above")
    print("  5. Mark Week 1 as COMPLETE")
    print("  6. Back")

    choice = input("\n  Choose (1-6): ").strip()

    if choice == '1':
        webbrowser.open_new_tab("https://kodekloud.com/courses/kubernetes-for-beginners/")
        print("  KodeKloud opened!")
    elif choice == '2':
        webbrowser.open_new_tab("https://kubernetes.io/docs/tutorials/")
        print("  K8s tutorials opened!")
    elif choice == '3':
        webbrowser.open_new_tab("https://learn.microsoft.com/en-us/azure/aks/")
        print("  AKS docs opened!")
    elif choice == '4':
        for url in config.get('learning_track', {}).get('resources', []):
            webbrowser.open_new_tab(url)
        print("  All resources opened!")
    elif choice == '5':
        config['learning_track']['started_k8s'] = True
        config['learning_track']['current_week'] = 2
        save_config(config)
        print(f" {CHECK} Week 1 marked complete! Moving to Week 2.")

    input("\n  Press Enter to continue...")


# ===================== REPORT =====================

def generate_report(config=None):
    if config is None:
        config = load_config()

    init_applications_csv()
    init_email_log_csv()

    apps = load_csv(DATA_DIR / "applications.csv")
    email_log = load_csv(DATA_DIR / "email_log.csv")
    jobs = load_csv(DATA_DIR / "Active_Job_Listings.csv")

    now = datetime.now()
    iso_cal = now.isocalendar()
    week_num = iso_cal[1]

    # Applications this week (approximate - same month)
    week_prefix = now.strftime("%Y-%m")
    week_apps = [a for a in apps if a.get('Date', '').startswith(week_prefix)] if apps else []
    week_emails = [e for e in email_log if e.get('Date', '').startswith(week_prefix)] if email_log else []

    report = f"""
+====================================================+
|   WEEKLY PROGRESS REPORT - Week {week_num}
+====================================================+

  Target:     {config['personal']['target_role']}
  Salary:     INR {config['preferences']['salary_expectation_min']//100000}-{config['preferences']['salary_expectation_max']//100000} LPA

  Applications Submitted: {len(apps) if apps else 0}
  Emails Sent:            {len(email_log) if email_log else 0}
  Active Job Targets:     {len(jobs) if jobs else 0}

  THIS MONTH:
  Applications: {len(week_apps)}
  Emails Sent:  {len(week_emails)}

  STATUS BREAKDOWN:"""
    if apps:
        statuses = {}
        for a in apps:
            s = a.get('Status', 'Unknown')
            statuses[s] = statuses.get(s, 0) + 1
        for s, c in sorted(statuses.items()):
            report += f"\n    {s}: {c}"
    else:
        report += "\n    No applications yet - Start today!"

    report += f"""

  RECENT EMAILS:"""
    if email_log:
        last5 = email_log[-5:] if len(email_log) >= 5 else email_log
        for e in last5:
            icon = check_icon(e.get('Status'))
            report += f"\n    {icon} {e.get('Date', '')[:10]} -> {e.get('Company', '')[:20]}"
    else:
        report += "\n    No emails sent yet"

    report += f"""

  NEXT ACTIONS:
    1. {'Send emails' if len(week_emails) == 0 else 'Emails done this month'}
    2. {'Apply to jobs' if len(week_apps) < 5 else 'Applications in progress'}
    3. {'Start K8s learning' if not config['learning_track']['started_k8s'] else 'Learning in progress'}
    4. Update LinkedIn profile and post

+====================================================+
"""
    print(report)

    report_path = LOGS_DIR / f"report_week_{week_num}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  Report saved to: {report_path}")


def check_icon(status):
    return "[OK]" if status == 'Sent' else "[NO]"


# ===================== SETUP =====================

def setup_wizard():
    print("\n" + "=" * 55)
    print("  FIRST-TIME SETUP WIZARD")
    print("=" * 55)

    config = load_config()

    print("\n  Step 1: Gmail App Password")
    print("  ---------------")
    print("  To send emails automatically, you need a Gmail App Password.")
    print("  1. Go to: https://myaccount.google.com/security")
    print("  2. Enable '2-Step Verification'")
    print("  3. Go to: https://myaccount.google.com/apppasswords")
    print("  4. Create app named 'DevOps Automation'")
    print("  5. Copy the 16-character password\n")

    pw = input("  Paste your App Password (or Enter to skip): ").strip()
    if pw:
        config['gmail']['app_password'] = pw
        print(f" {CHECK} App password saved!")

    print("\n  Step 2: Salary Expectations")
    print("  ---------------")
    min_sal = input(f"  Min salary LPA [{config['preferences']['salary_expectation_min']//100000}]: ").strip()
    max_sal = input(f"  Max salary LPA [{config['preferences']['salary_expectation_max']//100000}]: ").strip()

    if min_sal:
        config['preferences']['salary_expectation_min'] = int(min_sal) * 100000
    if max_sal:
        config['preferences']['salary_expectation_max'] = int(max_sal) * 100000

    print("\n  Step 3: AI Email Intelligence (Optional)")
    print("  ---------------")
    print("  Get a FREE Gemini API key at: https://aistudio.google.com/apikey")
    print("  Without it, emails use dynamic templates instead of AI.")
    print(f"  The key will be stored in: {BASE_DIR / '.env'}")
    print()

    # Check .env file for existing key
    env_path = BASE_DIR / ".env"
    existing_key = ""
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
            existing_key = os.getenv('GEMINI_API_KEY', '')
        except ImportError:
            pass

    if existing_key and existing_key != "YOUR_GEMINI_API_KEY_HERE":
        print(f" {CHECK} Gemini API key found in .env (showing: ...{existing_key[-4:]})")
        change = input("  Change API key? (press Enter to keep): ").strip()
        if change:
            existing_key = change
            # Write to .env
            with open(env_path, 'w') as f:
                f.write(f"# Gemini API Key\nGEMINI_API_KEY={existing_key}\n")
            print(f" {CHECK} .env file updated!")
            config['ai']['enabled'] = True
    else:
        new_key = input("  Paste your Gemini API key (or Enter to skip): ").strip()
        if new_key:
            with open(env_path, 'w') as f:
                f.write(f"# Gemini API Key - Get yours free at https://aistudio.google.com/apikey\nGEMINI_API_KEY={new_key}\n")
            print(f" {CHECK} Gemini API key saved to .env file!")
            config['ai']['enabled'] = True

    print("\n  Step 4: Resume Path")
    print("  ---------------")
    if os.path.exists(config['system']['resume_path']):
        print(f" {CHECK} Resume found at: {config['system']['resume_path']}")
    else:
        print(f" Resume not at: {config['system']['resume_path']}")
        new_path = input("  Enter correct path: ").strip()
        if new_path:
            config['system']['resume_path'] = new_path

    init_applications_csv()
    init_email_log_csv()
    save_config(config)

    print("\n" + "=" * 55)
    print(f" {CHECK} SETUP COMPLETE!")
    print("=" * 55)
    print("\n  WHAT TO DO NEXT:")
    print("  1. python app.py dashboard     -> See your stats")
    print("  2. python app.py launch-jobs   -> Start applying!")
    print("  3. python app.py blast         -> Send emails")
    print("  4. python app.py linkedin      -> Fix your profile\n")


# ===================== TASKS CHECKER =====================

def check_tasks(config=None):
    if config is None:
        config = load_config()

    today = datetime.now().strftime("%A")

    apps = load_csv(DATA_DIR / "applications.csv")
    email_log = load_csv(DATA_DIR / "email_log.csv")

    today_str = datetime.now().strftime("%Y-%m-%d")
    apps_today = sum(1 for a in apps if a.get('Date', '').startswith(today_str)) if apps else 0
    emails_today = sum(1 for e in email_log if e.get('Date', '').startswith(today_str)) if email_log else 0

    print(f"\nTODAY'S TASKS - {today}")
    print("=" * 55)

    print("\n  EVERY MORNING (5 min):")
    print("     python app.py dashboard  -> Check stats")

    day_tasks = {
        "Monday": [
            ("Send batch of cold emails (5-10)", emails_today >= 5),
            ("Post on LinkedIn (use Post 1 or Post 3)", False),
            ("Apply to 5+ jobs", apps_today >= 3),
        ],
        "Tuesday": [
            ("Send 5 more cold emails", emails_today >= 5),
            ("Connect with 5 recruiters on LinkedIn", False),
            ("K8s study: 15 min on KodeKloud", False),
        ],
        "Wednesday": [
            ("Post on LinkedIn (Post 2 or Post 7)", False),
            ("Apply to 5+ jobs", apps_today >= 3),
            ("Follow up on emails from last week", False),
        ],
        "Thursday": [
            ("Find 5 new emails via Hunter.io", False),
            ("Send 5 cold emails to new contacts", emails_today >= 3),
            ("K8s study: 15 min", False),
        ],
        "Friday": [
            ("Post on LinkedIn (Post 4 or Post 6)", False),
            ("python app.py report -> Weekly report", False),
            ("Apply to 5 jobs", apps_today >= 3),
        ],
        "Saturday": [
            ("Deep work: 1 hour K8s learning", False),
            ("python app.py dashboard -> Week progress", False),
            ("Send any pending follow-ups", False),
        ],
        "Sunday": [
            ("REST DAY! Relax and recharge", True),
            ("Plan next week's targets", False),
        ],
    }

    tasks = day_tasks.get(today, [])
    for task, done in tasks:
        status = DONE if done else PENDING
        print(f"     {status} {task}")

    print(f"\n  TODAY'S PROGRESS:")
    print(f"     Applications: {apps_today}")
    print(f"     Emails sent:  {emails_today}")

    all_done = all(done for _, done in tasks) if tasks else False
    if all_done:
        print(f"\n  ALL DONE FOR TODAY! Great work!")
    else:
        pending = [t for t, d in tasks if not d]
        print(f"\n  {len(pending)} tasks remaining. Let's go!")

    # Urgent reminders
    if today == "Monday" and emails_today == 0:
        print(f"\n  {WARN} No emails sent yet this week! Run:")
        print("     python app.py blast")
    if today == "Friday" and apps_today == 0:
        print(f"\n  {WARN} Apply to jobs NOW to hit weekly target!")

    print()


# ===================== UNIFIED AGENT =====================

def analyze_company(config=None):
    """Analyze a company: find matching jobs, contacts, ATS score, and outreach strategy."""
    if config is None:
        config = load_config()

    from intelligence import UnifiedAgent, ATSMatcher

    company = input("  Enter company name to analyze: ").strip()
    if not company:
        print(f" {CROSS} No company entered.")
        return

    agent = UnifiedAgent(config)
    ats = ATSMatcher()

    print(f"\n{'='*55}")
    print(f"  ANALYZING: {company}")
    print(f"{'='*55}")

    # Find matching jobs
    jobs = load_csv(DATA_DIR / "Active_Job_Listings.csv")
    company_jobs = [j for j in jobs if j.get('Company', '').lower() == company.lower()]

    if company_jobs:
        print(f"\n  MATCHING JOBS ({len(company_jobs)}):")
        print("-" * 40)
        for j in company_jobs:
            ms = j.get('Match_Score', 'N/A')
            title = j.get('Job_Title', 'N/A')
            link = j.get('Apply_Link', '')
            print(f"    {title:40s} | Match: {ms}")
            print(f"    Link: {link[:80]}")
            print()

            # ATS analysis
            analysis = ats.analyze(title, j.get('Notes', '') + ' ' + title)
            gap = analysis['missing_keywords']
            if gap:
                print(f"    ATS GAPS: {', '.join(gap[:5])}")
            print()
    else:
        print(f"\n  No job listings found for {company}.")

    # Find contacts
    contacts = load_csv(DATA_DIR / "Email_Contact_List.csv")
    company_contacts = [c for c in contacts if c.get('Company', '').lower() == company.lower()]

    if company_contacts:
        print(f"  CONTACTS ({len(company_contacts)}):")
        print("-" * 40)
        for c in company_contacts:
            name = c.get('Contact Name', 'N/A')
            title = c.get('Title', 'N/A')
            email = c.get('Email', 'N/A')
            conf = c.get('Email_Confidence', '')
            priority = c.get('Priority', '')
            print(f"    {name:25s} | {title:35s}")
            print(f"    Email: {email:40s} | {conf}")
            print(f"    Priority: {priority}")
            print()
    else:
        print(f"  No contacts found for {company}.")

    # Generate outreach suggestion
    result, error = agent.generate_outreach_email(company)
    if result:
        print(f"  AI OUTREACH SUGGESTION:")
        print("-" * 40)
        print(f"    Subject: {result['subject']}")
        print(f"    Body:")
        for line in result['email_body'].strip().split('\n'):
            print(f"      {line.strip()}")
        print()

    # Summary
    print(f"{'='*55}")
    print(f"  ACTION SUMMARY:")
    total_jobs = len(company_jobs)
    total_contacts = len(company_contacts)
    valid_contacts = sum(1 for c in company_contacts if c.get('Email', '') and 'PATTERN' not in c.get('Email', '').upper())

    print(f"  - Jobs found: {total_jobs}")
    print(f"  - Contacts found: {total_contacts} ({valid_contacts} with valid email)")
    print(f"  - To apply: python app.py launch-jobs  (then open {company}'s links)")
    print(f"  - To email: python app.py agent {company}")
    print(f"{'='*55}\n")


def agent_command(config=None, company_arg=None):
    """
    UNIFIED AGENT: Handles both jobs + recruiters for a company.
    Uses AI to generate personalized outreach.
    """
    if config is None:
        config = load_config()

    from intelligence import UnifiedAgent

    # Get company name
    company = company_arg
    if not company:
        company = input("  Enter company name for outreach: ").strip()
    if not company:
        print(f" {CROSS} No company entered.")
        return

    agent = UnifiedAgent(config)

    print(f"\n{'='*55}")
    print(f"  UNIFIED AGENT: {company}")
    print(f"{'='*55}")
    print(f"  AI Status: {'GEMINI ACTIVE' if agent.ai.available else 'FALLBACK MODE'}")
    print(f"  Analyzing jobs, contacts, and generating outreach...")

    # Preview the outreach
    result = agent.preview_outreach(company)

    if not result:
        print(f"\n  {CROSS} Could not generate outreach for {company}.")
        print(f"  Make sure the company exists in your job listings or contacts CSV.")
        print(f"  Try: python app.py analyze {company}")
        return

    # Ask to send
    choice = input(f"\n  Send this email to {result['contact'].get('Contact Name', 'recruiter')} at {company}? (type 'yes' to send): ").strip().lower()
    if choice != 'yes':
        print(f"  {CROSS} Cancelled.")
        return

    # Send
    email = result['contact'].get('Email', '').strip().lower()
    if not email or 'pattern' in email:
        print(f"  {CROSS} No valid email for {result['contact'].get('Contact Name', 'recruiter')}.")
        print(f"  Try connecting via LinkedIn InMail instead.")
        return

    print(f"  Sending to {result['contact'].get('Contact Name', '')} @ {company}...")

    body_html = f"""<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
{result['email_body'].replace(chr(10), '<br>').replace('<br><br>', '</p><p>') if result['email_body'] else ''}
</body></html>"""

    send_email(
        config, email, result['subject'], body_html,
        result['contact'].get('Contact Name', 'Recruiter'), company
    )


# ===================== MAIN =====================

def main():
    if not CONFIG_PATH.exists():
        print(f" {CROSS} config.json not found! Creating default...")
        print("   Run: python app.py setup")
        return

    if len(sys.argv) > 1:
        command = sys.argv[1]
        config = load_config()

        cmd_map = {
            'dashboard': show_dashboard,
            'blast': lambda: email_blaster(load_config()),
            'launch-jobs': lambda: launch_jobs(load_config()),
            'track': lambda: track_application(load_config()),
            'linkedin': lambda: linkedin_helper(load_config()),
            'learn': lambda: open_learning(load_config()),
            'report': lambda: generate_report(load_config()),
            'setup': setup_wizard,
            'followup': lambda: send_follow_ups(load_config()),
            'check-tasks': lambda: check_tasks(load_config()),
            'analyze': lambda: analyze_company(load_config()),
            'agent': lambda: agent_command(load_config(), sys.argv[2] if len(sys.argv) > 2 else None),
        }

        if command in cmd_map:
            cmd_map[command]()
        else:
            print(f" {CROSS} Unknown command: {command}")
            print("  Commands: dashboard, blast, launch-jobs, track, linkedin, learn, report, setup, followup, check-tasks, analyze, agent")
    else:
        while True:
            config = load_config()

            print("\n" + "=" * 55)
            print("  SOHAM'S PLACEMENT AUTOMATION HUB")
            print("  Your Personal Career Command Center")
            print("=" * 55)
            print(f"  {datetime.now().strftime('%A, %b %d, %Y')}")
            print("-" * 55)
            print("   1. Dashboard         -> See your stats")
            print("   2. Email Blaster     -> Send to ALL contacts")
            print("   3. Launch Jobs       -> Open jobs in browser")
            print("   4. Track Applications -> Log & update status")
            print("   5. LinkedIn Helper   -> Profile fixes + posts")
            print("   6. Learning Center   -> K8s & DevOps resources")
            print("   7. Weekly Report     -> Generate report")
            print("   8. Check Today's Tasks")
            print("   9. Send Follow-ups")
            print("  10. Analyze Company (jobs + contacts + ATS)")
            print("  11. Unified Agent (AI outreach for a company)")
            print("  12. Setup Wizard")
            print("  13. Exit")
            print("-" * 55)

            choice = input("  Choose (1-13): ").strip()

            menu = {
                '1': show_dashboard,
                '2': lambda: email_blaster(config),
                '3': lambda: launch_jobs(config),
                '4': lambda: track_application(config),
                '5': lambda: linkedin_helper(config),
                '6': lambda: open_learning(config),
                '7': lambda: generate_report(config),
                '8': lambda: check_tasks(config),
                '9': lambda: send_follow_ups(config),
                '10': lambda: analyze_company(config),
                '11': lambda: agent_command(config),
                '12': setup_wizard,
                '13': lambda: (print("\n  Goodbye! Keep pushing!\n"), sys.exit(0)),
            }

            if choice in menu:
                menu[choice]()
            else:
                print("  Invalid choice. Try 1-13.")


if __name__ == "__main__":
    main()
