"""
AI Intelligence Module - Dynamic Email Generation + Validation + Analysis
=========================================================================
Provides AI-powered personalization using Gemini API (free tier).
All email bodies are generated dynamically - NO hardcoded templates.
"""

import re
import json
import os
import csv
from datetime import datetime, timedelta

CHECK = "[OK]"
CROSS = "[XX]"
WARN = "[!!]"
STAR = "[*]"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# ===================== EMAIL VALIDATOR =====================

class EmailValidator:
    """Validates email addresses with syntax check + MX record verification."""

    @staticmethod
    def validate_syntax(email):
        """Basic email syntax validation."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def validate_mx(domain):
        """Check if domain has MX records (email can be delivered)."""
        try:
            import dns.resolver
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                return len(mx_records) > 0
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                    dns.resolver.LifetimeTimeout, dns.exception.Timeout):
                return False
            except ImportError:
                # dnspython not installed - skip MX check
                return None
        except ImportError:
            return None

    @staticmethod
    def is_disposable(domain):
        """Check if domain is a known disposable email provider."""
        disposable = [
            'mailinator.com', 'guerrillamail.com', '10minutemail.com',
            'tempmail.com', 'throwaway.email', 'yopmail.com',
            'sharklasers.com', 'trashmail.com', 'temp-mail.org',
            'fakeinbox.com', 'mailnator.com', 'dispostable.com'
        ]
        return domain.lower() in disposable

    def validate(self, email):
        """Full email validation. Returns dict with status and details."""
        email = email.strip().lower()
        result = {
            'email': email,
            'valid': False,
            'syntax_ok': False,
            'mx_ok': False,
            'disposable': False,
            'score': 0,
            'issues': []
        }

        # Syntax check
        if not self.validate_syntax(email):
            result['issues'].append('Invalid email format')
            return result
        result['syntax_ok'] = True
        result['score'] += 40

        # Domain extraction
        domain = email.split('@')[1]

        # Disposable check
        if self.is_disposable(domain):
            result['disposable'] = True
            result['issues'].append('Disposable email domain')
            result['score'] = 10
            return result

        # MX record check
        mx_result = self.validate_mx(domain)
        if mx_result is True:
            result['mx_ok'] = True
            result['score'] += 60
            result['valid'] = True
        elif mx_result is None:
            # MX check unavailable, pass based on syntax
            result['mx_ok'] = None
            result['score'] += 30
            result['valid'] = True  # Assume valid if syntax passes
        else:
            result['issues'].append(f'No MX records for {domain}')
            result['score'] += 10

        return result


# ===================== SPAM CHECKER =====================

class SpamChecker:
    """Detects spam trigger words and patterns in email content."""

    HIGH_RISK_WORDS = [
        'free', 'act now', 'limited time', 'congratulations', 'winner',
        'click here', 'urgent', 'guaranteed', 'exclusive deal', 'buy now',
        'cash', 'earn money', 'work from home', 'no cost', 'risk free',
        'double your', 'amazing', 'incredible', 'once in a lifetime'
    ]

    MEDIUM_RISK_WORDS = [
        'opportunity', 'great', 'best', 'excellent', 'unique',
        'special', 'now', 'today', 'don\'t delete', 'read this',
        'important', 'please read', 'information you requested',
        'not spam', 'remove', 'stop'
    ]

    @staticmethod
    def check_spam_score(text):
        """Analyze text for spam characteristics. Returns score and issues."""
        text_lower = text.lower()
        score = 0
        issues = []

        # Check for all-caps words (shouting)
        caps_words = re.findall(r'\b[A-Z]{4,}\b', text)
        if len(caps_words) > 3:
            score += 20
            issues.append(f'Excessive use of ALL CAPS ({len(caps_words)} words)')

        # Check for excessive exclamation marks
        excl_count = text.count('!')
        if excl_count > 3:
            score += 10
            issues.append(f'Too many exclamation marks ({excl_count})')

        # Check for excessive links
        link_count = len(re.findall(r'https?://', text))
        if link_count > 3:
            score += 15
            issues.append(f'Too many links ({link_count})')

        # Check high-risk words
        found_high = [w for w in SpamChecker.HIGH_RISK_WORDS if w in text_lower]
        if found_high:
            score += 25
            issues.append(f'High-risk words found: {", ".join(found_high[:3])}')

        # Check medium-risk words
        found_med = [w for w in SpamChecker.MEDIUM_RISK_WORDS if w in text_lower]
        if found_med:
            score += min(len(found_med) * 5, 20)
            if len(found_med) > 3:
                issues.append(f'Marketing tone detected ({len(found_med)} trigger words)')

        # Check HTML-to-text ratio
        html_tags = len(re.findall(r'<[^>]+>', text))
        text_len = len(re.sub(r'<[^>]+>', '', text))
        if html_tags > 0 and text_len > 0:
            ratio = html_tags / text_len
            if ratio > 0.5:
                score += 10
                issues.append('High HTML-to-text ratio')

        return {
            'spam_score': min(score, 100),
            'is_spammy': score >= 50,
            'issues': issues,
            'grade': 'PASS' if score < 30 else 'WARN' if score < 50 else 'FAIL'
        }


# ===================== ATS MATCHER =====================

class ATSMatcher:
    """Analyzes resume-job fit by keyword matching."""

    RESUME_KEYWORDS = [
        'ansible', 'terraform', 'azure', 'jenkins', 'docker', 'python',
        'prometheus', 'grafana', 'logicmonitor', 'ci/cd', 'gitlab',
        'servicenow', 'bigpanda', 'linux', 'shell', 'powershell',
        'automation', 'infrastructure as code', 'iam', 'vnet',
        'monitoring', 'incident management', 'agile', 'scrum',
        'git', 'yaml', 'json', 'rest api', 'bash', 'networking'
    ]

    @staticmethod
    def extract_job_keywords(job_title, job_notes):
        """Extract keywords from job title and notes."""
        text = f"{job_title} {job_notes}".lower()
        found = []
        for kw in ATSMatcher.RESUME_KEYWORDS:
            if kw in text:
                found.append(kw)
        return found

    @staticmethod
    def match_score(resume_keywords, job_keywords):
        """Calculate match percentage between resume and job keywords."""
        if not job_keywords:
            return 0, []
        matched = [kw for kw in job_keywords if kw in resume_keywords]
        missing = [kw for kw in job_keywords if kw not in resume_keywords]
        score = int((len(matched) / len(job_keywords)) * 100)
        return score, missing

    def analyze(self, job_title, job_notes):
        """Full ATS analysis for a job listing."""
        resume_keywords = self.RESUME_KEYWORDS
        job_keywords = self.extract_job_keywords(job_title, job_notes)
        score, missing = self.match_score(resume_keywords, job_keywords)

        return {
            'match_score': score,
            'job_keywords_found': job_keywords,
            'matched_keywords': [kw for kw in job_keywords if kw in resume_keywords],
            'missing_keywords': missing,
            'gap_severity': 'LOW' if score >= 70 else 'MEDIUM' if score >= 50 else 'HIGH',
            'suggestions': [
                f"Add '{kw}' to your resume if you have experience" for kw in missing[:5]
            ]
        }


# ===================== AI EMAIL GENERATOR =====================

class AIEmailGenerator:
    """
    Uses Google Gemini API (free tier) to DYNAMICALLY generate
    personalized email bodies. NO hardcoded templates.
    Falls back to a basic dynamic template if AI is unavailable.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model = None
        self.available = False

        # Priority: parameter > .env file > config.json
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            try:
                from dotenv import load_dotenv
                env_path = os.path.join(os.path.dirname(__file__), '.env')
                if os.path.exists(env_path):
                    load_dotenv(env_path)
                    env_key = os.getenv('GEMINI_API_KEY')
                    if env_key and env_key != "YOUR_GEMINI_API_KEY_HERE":
                        api_key = env_key
                        self.api_key = env_key  # Update tracked key
            except ImportError:
                pass

        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                self.model_name = 'gemini-2.0-flash'
                self.available = True
            except Exception as e:
                print(f"  {WARN} Gemini init failed: {e}")
                print(f"  Will use dynamic template fallback instead.")

    def generate_email(self, recruiter_name, company, role_title,
                       recruiter_notes="", job_highlights=""):
        """
        DYNAMICALLY generates a personalized email using AI.
        Every call produces unique content based on the inputs.
        NO hardcoded templates.
        """
        if self.available and self.model:
            return self._ai_generate(recruiter_name, company, role_title,
                                     recruiter_notes, job_highlights)
        else:
            return self._dynamic_fallback(recruiter_name, company, role_title,
                                          recruiter_notes, job_highlights)

    def _ai_generate(self, recruiter_name, company, role_title,
                     recruiter_notes, job_highlights):
        """Generate using Gemini AI - fully dynamic."""
        prompt = f"""You are a career coach writing a professional cold email for a DevOps Engineer.

CONTEXT:
- Sender: Soham Deshmukh, DevOps Engineer at Wipro (3 years experience)
- Recipient: {recruiter_name}, a recruiter/talent acquisition professional at {company}
- Recruiter background: {recruiter_notes or 'Not specified'}
- Role applied for: {role_title} at {company}
- Job requirements/highlights: {job_highlights or 'Not specified'}
- Sender's top skills: Ansible, Terraform, Azure, Jenkins, Docker, Python, Prometheus/Grafana, LogicMonitor, CI/CD, ServiceNow
- Key achievement: Built an auto-remediation platform that reduced manual incident handling by ~40%
- Also pursuing M.Tech at BITS Pilani while working full-time

WRITING RULES:
1. Write a professional email (3-4 short paragraphs, max 200 words)
2. Reference the specific recruiter context if available (make it personal)
3. Reference the specific role they applied for
4. Include 2-3 relevant skills that match the role
5. Mention the 40% metric naturally
6. End with a clear call to action (15-minute chat)
7. Tone: professional, confident, not desperate
8. NO generic phrases like "I came across your profile"
9. Make each sentence count - no fluff

Return ONLY the email body. No subject line. No explanations."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip() if response.text else None
        except Exception as e:
            print(f"  {WARN} AI generation failed: {e}")
            return self._dynamic_fallback(recruiter_name, company, role_title,
                                          recruiter_notes, job_highlights)

    def generate_subject(self, company, role_title, recruiter_name=None):
        """Generate a dynamic subject line using AI."""
        if not self.available:
            return self._subject_fallback(company, role_title)

        prompt = f"""Generate ONE professional email subject line for a DevOps Engineer named Soham applying to {role_title} at {company}.
Rules: Max 10 words, professional tone, include the role name, NO clickbait.
Return ONLY the subject line, nothing else."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except:
            return self._subject_fallback(company, role_title)

    def generate_followup(self, recruiter_name, company, role_title, original_email):
        """Generate a dynamic follow-up email based on the previous email."""
        if not self.available:
            return self._followup_fallback(recruiter_name, company)

        prompt = f"""Write a short follow-up email (2 paragraphs) for Soham, a DevOps Engineer, following up on his application for {role_title} at {company}.
Recipient: {recruiter_name}
Original email was about his application.
Tone: polite, professional, not pushy. Reference the original application.
End with a call to action.
Max 100 words. Return ONLY the body."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except:
            return self._followup_fallback(recruiter_name, company)

    def _dynamic_fallback(self, recruiter_name, company, role_title,
                          recruiter_notes, job_highlights):
        """Fallback that generates a dynamic email (no AI, but not hardcoded).
        Uses recruiter notes and job details to create varied content each time."""
        first_name = recruiter_name.split()[0] if recruiter_name else "there"

        # Build dynamic skill selection - different each time
        skills_pool = [
            "Ansible (AAP/Tower) for configuration management",
            "Terraform + Azure for infrastructure as code",
            "CI/CD pipelines with Jenkins, Docker, and GitLab",
            "Python automation and event-driven remediation",
            "Prometheus, Grafana, and LogicMonitor for observability",
            "Automated ServiceNow ticketing via Ansible AAP API integration",
            "Multi-environment IaC deployment on Azure using Terraform",
            "End-to-end CI/CD pipeline design with automated testing",
        ]

        import random
        selected = random.sample(skills_pool, min(3, len(skills_pool)))

        # Intelligently extract usable recruiter info from notes
        personal_line = ""
        if recruiter_notes:
            # Remove metadata prefixes for cleaner reading
            clean_notes = recruiter_notes
            for prefix in ['PUBLICLY POSTED:', 'CONFIRMED -', 'HIGH -', 'Unable to', 'Partial name']:
                clean_notes = clean_notes.replace(prefix, '')
            clean_notes = clean_notes.strip(' ".,;:')

            # Extract a usable personalization hook
            if 'background' in clean_notes.lower():
                personal_line = f"I saw your background in talent acquisition and wanted to reach out about the {role_title} role."
            elif 'recruiter' in clean_notes.lower() or 'talent' in clean_notes.lower():
                personal_line = f"I noticed your work in tech recruiting and wanted to connect about the {role_title} position at {company}."
            elif 'linkedin' in clean_notes.lower():
                personal_line = f"I came across your profile and wanted to reach out regarding the {role_title} opportunity at {company}."
            elif len(clean_notes) > 10:
                personal_line = f"Reaching out about the {role_title} role at {company}. I have applied and wanted to introduce myself."
            else:
                personal_line = f"I am writing regarding the {role_title} position at {company}."
        else:
            personal_line = f"I am writing regarding the {role_title} position at {company} and would love to connect."

        body = f"""Hi {first_name},

{personal_line}

I am a DevOps Engineer at Wipro with 3 years of hands-on experience building automation and infrastructure solutions. My core expertise includes:

- {' | '.join(selected)}

A key achievement I am proud of: I built an automated incident remediation platform integrating LogicMonitor, BigPanda, Jenkins, Docker, ServiceNow, and Ansible AAP. This reduced manual incident handling by approximately 40 percent and cut infrastructure reporting time from over 3 hours to under 1 minute.

I am also pursuing my M.Tech at BITS Pilani while working full-time, which has strengthened my ability to manage complex projects under tight deadlines.

Would you have 10-15 minutes this week for a quick conversation? My resume is attached.

Best regards,
Soham Deshmukh
+91-9503024323
linkedin.com/in/soham-deshmukh-142939225"""

        return body.strip()

    def _subject_fallback(self, company, role_title):
        """Fallback subject line generation."""
        subjects = [
            f"Application: {role_title} at {company} | Soham Deshmukh",
            f"{role_title} - 3 YOE Ansible/Terraform/Azure | {company} Application",
            f"DevOps Engineer ({role_title}) | {company} | Soham Deshmukh",
        ]
        import random
        return random.choice(subjects)

    def _followup_fallback(self, recruiter_name, company):
        """Fallback follow-up email."""
        first_name = recruiter_name.split()[0] if recruiter_name else "there"
        return f"""Hi {first_name},

I wanted to follow up on my previous application for the role at {company}. I remain very interested in the opportunity and believe my experience with Ansible, Terraform, and Azure automation could bring value to your team.

Would you have a few minutes to connect this week?

Best,
Soham Deshmukh"""


# ===================== SEND OPTIMIZER =====================

class SendOptimizer:
    """Optimizes email send timing for maximum open rates."""

    @staticmethod
    def best_time_to_send():
        """Returns the best time to send based on research data."""
        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()

        # Best hours: Tue-Thu, 8-11am or 1-3pm (proven highest open rates)
        if weekday >= 5:  # Weekend
            return {
                'should_send': False,
                'reason': 'Weekend - low open rates. Schedule for Monday.',
                'suggested_time': 'Monday 9:00 AM'
            }
        if hour < 6 or hour > 20:
            return {
                'should_send': False,
                'reason': f'Outside business hours ({hour}:00).',
                'suggested_time': 'Next business morning 9:00 AM'
            }
        if hour < 8:
            return {
                'should_send': True,
                'reason': 'Early morning - good, but best after 8AM.',
                'suggested_time': None
            }
        if 12 <= hour < 13:
            return {
                'should_send': True,
                'reason': 'Lunch hour - moderate open rates.',
                'suggested_time': None
            }
        if 17 <= hour <= 20:
            return {
                'should_send': True,
                'reason': 'Evening - acceptable, but morning is better.',
                'suggested_time': 'Tomorrow 9:00 AM'
            }
        # Prime hours: 8-11am, 1-5pm on weekdays
        return {
            'should_send': True,
            'reason': 'Prime sending time - high open rates expected.',
            'suggested_time': None
        }

    @staticmethod
    def should_send_now():
        """Quick check if we should send now."""
        info = SendOptimizer.best_time_to_send()
        return info['should_send']


# ===================== RECRUITER RESEARCH HELPER =====================

class RecruiterResearcher:
    """Provides research suggestions and data for recruiters."""

    @staticmethod
    def get_personalization_hints(recruiter_notes, company):
        """Extract personalization hooks from recruiter notes."""
        hints = []
        notes_lower = recruiter_notes.lower() if recruiter_notes else ""

        if 'barclays' in notes_lower:
            hints.append("Has Barclays background - mention services/consulting connection")
        if '11 year' in notes_lower or '11+ year' in notes_lower:
            hints.append("Long tenure at previous company - acknowledge career commitment")
        if 'public' in notes_lower and 'post' in notes_lower:
            hints.append("Actively posted on LinkedIn asking for resumes - reference this")
        if 'certification' in notes_lower or 'certified' in notes_lower:
            hints.append("Has professional certifications - mention your BITS Pilani M.Tech")
        if 'external' in notes_lower or 'recruited for' in notes_lower:
            hints.append("Previously recruited for this company externally - know the company well")
        if 'manager' in notes_lower:
            hints.append("Manager-level recruiter - they make hiring decisions")

        if not hints:
            hints.append(f"Research {company} recent news/projects for personalization")

        return hints


# ===================== UNIFIED AGENT =====================

class UnifiedAgent:
    """
    Single unified agent that handles both jobs AND recruiters.
    Uses AI for all communication generation.
    """

    def __init__(self, config):
        self.config = config
        self.ai = AIEmailGenerator(
            config.get('ai', {}).get('gemini_api_key')
        )
        self.validator = EmailValidator()
        self.spam_checker = SpamChecker()
        self.ats = ATSMatcher()
        self.optimizer = SendOptimizer()
        self.researcher = RecruiterResearcher()

    def analyze_company(self, company_name):
        """Analyze a company: find jobs + contacts + generate outreach plan."""
        jobs = self._load_jobs()
        contacts = self._load_contacts()

        company_jobs = [j for j in jobs if j.get('Company', '').lower() == company_name.lower()]
        company_contacts = [c for c in contacts if c.get('Company', '').lower() == company_name.lower()]

        result = {
            'company': company_name,
            'jobs': company_jobs,
            'contacts': company_contacts,
            'ats_analysis': [],
            'personalization_hints': []
        }

        for job in company_jobs:
            ats = self.ats.analyze(
                job.get('Job_Title', ''),
                job.get('Notes', '') + ' ' + job.get('Job_Title', '')
            )
            result['ats_analysis'].append({
                'title': job.get('Job_Title', ''),
                'match': ats
            })

        for contact in company_contacts:
            hints = self.researcher.get_personalization_hints(
                contact.get('Notes', ''),
                company_name
            )
            result['personalization_hints'].append({
                'name': contact.get('Contact Name', ''),
                'title': contact.get('Title', ''),
                'email': contact.get('Email', ''),
                'hints': hints
            })

        return result

    def generate_outreach_email(self, company_name, contact_name=None):
        """
        Generate a complete outreach email for a company.
        Automatically finds the best job + contact match.
        """
        analysis = self.analyze_company(company_name)
        contacts = analysis['contacts']
        jobs = analysis['jobs']
        ats_analyses = analysis['ats_analysis']

        if not contacts and not jobs:
            return None, "No jobs or contacts found for this company."

        # Pick the best contact
        target_contact = None
        if contacts:
            # Prefer high-priority contacts
            for c in contacts:
                p = c.get('Priority', '3')
                if str(p).startswith('1'):
                    target_contact = c
                    break
            if not target_contact:
                target_contact = contacts[0]

        # Pick the best job (highest match score) for this company
        target_job = None
        best_match = 0
        for job in jobs:
            if job.get('Company', '').lower() != company_name.lower():
                continue
            ms = job.get('Match_Score', '0').replace('%', '')
            if ms.isdigit() and int(ms) > best_match:
                best_match = int(ms)
                target_job = job

        # If we have a contact but no specific job match, use a fallback
        if target_contact and not target_job:
            target_job = {'Company': company_name, 'Job_Title': 'DevOps Engineer', 'Notes': ''}

        if not target_contact and target_job:
            return None, f"Job found but no recruiter contact for {company_name}."

        if not target_contact:
            return None, f"No contacts available for {company_name}."

        contact_name = target_contact.get('Contact Name', 'Hiring Manager')
        role_title = target_job.get('Job_Title', 'DevOps Engineer') if target_job else 'DevOps Engineer'
        recruiter_notes = target_contact.get('Notes', '')
        job_highlights = target_job.get('Notes', '') if target_job else ''

        # Validate email
        email = target_contact.get('Email', '').strip().lower()
        validation = self.validator.validate(email) if email else {'valid': False, 'issues': ['No email']}

        # Generate AI email
        email_body = self.ai.generate_email(
            contact_name, company_name, role_title,
            recruiter_notes, job_highlights
        )

        # Generate subject line
        subject = self.ai.generate_subject(company_name, role_title, contact_name)

        # Combined result
        return {
            'contact': target_contact,
            'job': target_job,
            'email_body': email_body,
            'subject': subject,
            'email_validation': validation,
            'ats_analysis': ats_analyses[0] if ats_analyses else None,
            'personalization_hints': self.researcher.get_personalization_hints(
                recruiter_notes, company_name
            )
        }, None

    def preview_outreach(self, company_name):
        """Preview what would be sent for a company."""
        result, error = self.generate_outreach_email(company_name)
        if error:
            print(f"  {CROSS} {error}")
            return

        contact = result['contact']
        job = result['job']

        print(f"\n{'='*55}")
        print(f"  OUTREACH PLAN: {company_name}")
        print(f"{'='*55}")
        print(f"  CONTACT:  {contact.get('Contact Name', 'N/A')} ({contact.get('Title', 'N/A')})")
        print(f"  EMAIL:    {contact.get('Email', 'N/A')}")
        print(f"  ROLE:     {job.get('Job_Title', 'N/A') if job else 'N/A'}")

        if result.get('ats_analysis'):
            ats = result['ats_analysis']['match']
            print(f"  ATS MATCH: {ats['match_score']}%")
            if ats['missing_keywords']:
                print(f"  GAPS:     {', '.join(ats['missing_keywords'][:3])}")

        if result['email_validation']['valid']:
            print(f"  EMAIL:    {CHECK} Valid")
        else:
            print(f"  EMAIL:    {CROSS} Issues: {', '.join(result['email_validation']['issues'])}")

        print(f"\n  SUBJECT:  {result['subject']}")
        print(f"\n  EMAIL BODY:")
        print(f"  {'-'*50}")
        for line in result['email_body'].split('\n'):
            print(f"  {line.strip()}")
        print(f"  {'-'*50}")

        # Spam check
        spam = self.spam_checker.check_spam_score(result['email_body'])
        if spam['grade'] == 'PASS':
            print(f"\n  SPAM CHECK: {CHECK} {spam['grade']} (score: {spam['spam_score']})")
        elif spam['grade'] == 'WARN':
            print(f"\n  SPAM CHECK: {WARN} {spam['grade']} (score: {spam['spam_score']})")
            for issue in spam['issues']:
                print(f"             {issue}")
        else:
            print(f"\n  SPAM CHECK: {CROSS} {spam['grade']} (score: {spam['spam_score']})")
            for issue in spam['issues']:
                print(f"             {issue}")

        # Send timing
        timing = self.optimizer.best_time_to_send()
        if timing['should_send']:
            print(f"  TIMING:   {CHECK} {timing['reason']}")
        else:
            print(f"  TIMING:   {WARN} {timing['reason']}")
            if timing.get('suggested_time'):
                print(f"             Best to send: {timing['suggested_time']}")

        print(f"{'='*55}\n")
        return result

    def send_outreach(self, company_name):
        """Full outreach flow: preview -> approve -> send."""
        result, error = self.generate_outreach_email(company_name)
        if error:
            print(f"  {CROSS} {error}")
            return False

        # Preview first
        result = self.preview_outreach(company_name)
        if not result:
            return False

        # Approve
        choice = input("  Send this email now? (type 'yes' to send): ").strip().lower()
        if choice != 'yes':
            print(f"  {CROSS} Cancelled.")
            return False

        # Send
        from app import send_email
        send_email(
            self.config,
            result['contact']['Email'],
            result['subject'],
            result['email_body'],
            result['contact']['Contact Name'],
            company_name
        )
        return True

    def _load_jobs(self):
        """Load job listings from CSV."""
        path = os.path.join(DATA_DIR, "Active_Job_Listings.csv")
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _load_contacts(self):
        """Load email contacts from CSV."""
        path = os.path.join(DATA_DIR, "Email_Contact_List.csv")
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
