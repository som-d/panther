# Interview Prep — Monitoring & Observability Engineer @ ParentPay Group

## Target: ₹11-12 LPA

---

## SECTION 1: LOGICMONITOR (Advanced)

### Q1: Explain LogicMonitor architecture — collectors, collectors groups, device groups, data sources.

**Answer:**
LogicMonitor has a simple architecture. Collectors are software agents installed on Windows or Linux servers inside your network. They do the polling. They connect outbound to LM cloud on port 443. No inbound ports needed.

Collector groups let you organize collectors by location or function. For example, one collector group for Pune DC, another for Mumbai DC.

Device groups organize monitored devices. You can nest them. Properties set at the group level get inherited by all child devices.

DataSources are monitoring templates. Each DataSource has one or more DataPoints. For example, CPU data source has datapoints like total cpu, user cpu, system cpu. Each DataSource can run on specific OIDs, scripts, or commands.

---

### Q2: How do you create a custom DataSource?

**Answer:**
I created a custom DataSource for Linux process monitoring using SNMP. The script walks the hrSWRunTable via HOST-RESOURCES-MIB, finds matching process names, and returns CPU, memory, process count, and status. It handles cases where a process has multiple PIDs.

To create one: go to Settings > LogicModules > Add > DataSource. Choose Active Discovery for the discovery script. Write a collection script (Groovy, Python, or PowerShell). Set the polling interval. Define datapoints. Apply alert thresholds. Test on a device, then commit.

---

### Q3: How does LM authentication work? Explain LMv1 API.

**Answer:**
LMv1 uses HMAC-SHA256 signing. You have an Access ID and Access Key. To make a request:

1. Get current time in milliseconds
2. Concatenate: HTTP method + epoch + request body + resource path
3. HMAC-SHA256 that string using your Access Key
4. Base64 encode the hex digest
5. Send it in Authorization header: "LMv1 {AccessId}:{signature}:{epoch}"

I wrote Python scripts that handle this. I also used the API with Ansible for dynamic IP updates and to add ping monitoring.

---

### Q4: How do you handle alert fatigue in LogicMonitor?

**Answer:**
Several ways:

- **Alert thresholds** — set appropriate thresholds, not too sensitive
- **Dependency aware alerts** — if parent device is down, suppress child alerts
- **Alert rollup** — group related alerts into one
- **Alert rules** — route different alerts to different teams based on severity
- **SDT (Scheduled Down Time)** — suppress alerts during maintenance windows
- **Escalation chains** — delays before escalating to next level

I used BigPanda for event correlation on top of LM to further reduce noise by grouping related alerts into incidents.

---

### Q4b: Explain how LM alert rules and escalation chains work in detail.

**Answer:**

**Alert Rules** in LM let you control what happens when an alert fires. Think of them as if-this-then-that for alerts. For example:
- IF severity is "critical" AND device group is "production" THEN send to PagerDuty and email ops-team@
- IF alert is "warning" THEN create a low-priority ticket only
- IF alert clears automatically THEN close the associated ticket

Each rule has:
1. **Filters** — match on severity (critical/error/warning), device group, datasource, datapoint
2. **Actions** — send email, trigger webhook, push to ITSM, create SDT, run remote script
3. **Escalation** — if alert isn't acknowledged in N minutes, escalate to next level

**Escalation Chains** define who gets contacted in what order, and how long to wait before escalating:

Level 1 (0-5 min): Primary on-call engineer → SMS + phone
Level 2 (5-15 min): Team lead → phone
Level 3 (15-30 min): Manager → phone + email
Level 4 (30+ min): Director / major incident process triggered

I configured escalation chains so that overnight alerts go through 3 levels before waking up senior management. This prevents unnecessary escalation for false alarms but ensures nothing slips through for real issues.

In my role, I helped design the alert rules so that:
- Infrastructure alerts (CPU, disk) → go to L1 infrastructure team
- Application alerts → go to application team with different severity
- Critical alerts that match known patterns → trigger Ansible auto-remediation webhook first
- If auto-remediation fails → escalate to human on-call

---

### Q5: How do you scale collectors in a large environment?

**Answer:**
One collector can handle about 1000 devices or 5000 datapoints depending on polling interval. When we grow beyond that, we add more collectors.

Steps:
1. Deploy a new collector VM (redundant pair recommended)
2. Assign it to a collector group (e.g., "Pune DC")
3. Move device groups to that collector group
4. Monitor collector load under Manage > Collectors > Capacity

For redundancy, we deploy collector failover pairs. The primary collector sends heartbeat, and if it stops, the failover takes over.

---

### Q6: What are properties in LogicMonitor and how do they propagate?

**Answer:**
Properties are key-value pairs attached to devices or device groups. Examples: `location=Pune`, `environment=production`, `system.azure.region=eastus`.

When you set a property at a device group level, all child devices inherit it. This is called property propagation. It helps with:
- Auto-assigning alert thresholds
- Routing alerts to the right team
- Grouping dashboards
- Configuring collector assignment

I used custom properties on device groups so all servers in a group automatically get the correct monitoring profile.

---

### Q7: What is Active Discovery in LM?

**Answer:**
Active Discovery is how LM finds what to monitor on a device automatically. For example, for a Windows server, it auto-discovers all disk drives. For Linux, it discovers network interfaces.

The discovery script runs and returns a list of instances. Each instance becomes a separate monitoring entity. For my custom process monitor, the discovery script returns the list of process names found, and the collection script monitors each.

---

### Q8: What is the difference between a DataSource, ConfigSource, EventSource, and PropertySource?

**Answer:**
- **DataSource** — collects performance metrics (CPU, memory, disk, process state)
- **ConfigSource** — collects configuration files for drift detection
- **EventSource** — collects log events and matches patterns
- **PropertySource** — auto-assigns properties to devices based on discovery results

---

### Q9: How do you monitor network devices with LM?

**Answer:**
LM monitors network devices via SNMP. You add the device by IP, provide SNMP community string (v2c) or credentials (v3). LM auto-discovers interfaces, CPU, memory, and inventory. You can set up bandwidth utilization graphs, interface status alerts, and error/discard monitoring.

---

### Q10: How do you troubleshoot a failing DataSource?

**Answer:**
1. Check the device is reachable (ping, SNMP test)
2. Run the DataSource manually from the device page
3. Check collector logs for errors
4. Verify SNMP credentials or script dependencies
5. Test the script or command locally on the collector
6. Check if any required OIDs are missing on the target

---

## SECTION 2: API INTEGRATIONS

### Q11: What REST API integrations have you built with LogicMonitor?

**Answer:**
I built three integrations:

1. **LM API + Python** — Added ping monitoring for URLs automatically. The script handles HMAC-SHA256 auth, constructs JSON payload, posts to LM.

2. **LM API + Ansible** — Dynamic IP updates. When a server's IP changes, Ansible playbook triggers the LM API to update the device details.

3. **LM API + Python** — Created service monitoring and URL monitoring programmatically instead of using the UI.

---

### Q12: Explain webhooks and how you'd use them in monitoring.

**Answer:**
A webhook is an HTTP callback. When an alert fires in LM, it sends an HTTP POST with a JSON payload to a URL you configure. The receiving system (Slack, Teams, ServiceNow, Ansible Tower) processes it.

I used webhooks for auto-remediation. When LM detected a critical alert, it sent a webhook to Ansible Tower, which ran a playbook to fix the issue. This reduced manual incidents by 40%.

---

### Q13: How would you integrate LM with ServiceNow?

**Answer:**
Two approaches:

1. **LM sends webhook** to ServiceNow REST API when alert fires → creates incident
2. **ServiceNow polls** LM API periodically for active alerts

The webhook approach is real-time. The integration flow works like this:

**Step-by-step:**
1. In LM, create an Alert Rule with action type "Webhook"
2. Set the URL to ServiceNow REST API endpoint: `https://{instance}.service-now.com/api/now/table/incident`
3. Configure the webhook payload as JSON with these fields:
   - `short_description` — alert message
   - `description` — device name + datapoint + threshold value
   - `category` = "monitoring"
   - `assignment_group` — based on device group (infra/app/network)
   - `urgency` = mapped from LM severity (critical=1, error=2, warning=3)
4. ServiceNow authenticates via Basic Auth (username/password) or OAuth
5. When alert clears, LM sends another webhook to update the incident state to "Resolved"

**Bidirectional sync:** ServiceNow can also update LM when an incident is acknowledged, so LM knows a human is looking at it.

**What I've actually done:** I integrated LM with Ansible Tower via webhooks for auto-remediation. I understand the ServiceNow REST API pattern well enough to set up the same — the concepts are identical: webhook → REST endpoint → JSON payload → authentication.

---

### Q14: What's the difference between REST and SOAP?

**Answer:**
- **REST** — lightweight, uses JSON, HTTP methods (GET/POST/PUT/DELETE), stateless. What LM uses.
- **SOAP** — XML-based, heavier, has strict standards, uses WSDL. Older systems use it.

Most modern APIs including LM, ServiceNow, Slack, Teams are REST.

---

### Q15: How do you handle API rate limiting?

**Answer:**
When an API has a rate limit (e.g., 100 requests per minute), I:
1. Add delays between requests using `time.sleep()`
2. Check response headers for rate limit info
3. Implement retry logic with exponential backoff
4. Batch operations where possible

---

## SECTION 3: END USER MONITORING

### Q16: What is end user monitoring? Explain synthetic vs RUM.

**Answer:**
End user monitoring measures the experience from the user's perspective, not from the server side.

- **Synthetic monitoring** — runs scripted tests from bots. It simulates a user journey (login, search, checkout). Runs on a schedule from different locations. Catches problems before users do.
- **RUM (Real User Monitoring)** — captures actual user browser data. It measures real page loads, clicks, errors. Gives you what real users actually experienced.

Synthetic is proactive. RUM is reactive but shows reality. Use both.

---

### Q17: How would you set up URL monitoring for a website?

**Answer:**
I already did this with LM using the Python API. I'd create an HTTP/HTTPS check that:
1. Hits the URL at regular intervals (every 1-5 minutes)
2. Checks response status code (expect 200)
3. Validates response time (alert if > 3 seconds)
4. Optionally checks for text in the response body
5. Alerts on failure or slow response

For a full user journey, I'd use a synthetic tool that can log in, navigate pages, and verify content.

---

### Q18: What are the golden signals of monitoring?

**Answer:**
The four golden signals from Google SRE:
1. **Latency** — how long it takes to respond
2. **Traffic** — how many requests are coming in
3. **Errors** — rate of failed requests (5xx, 4xx)
4. **Saturation** — how full your resources are (CPU, memory, disk, connections)

For end user monitoring, latency and errors are the most important signals.

---

### Q19: What's the difference between availability and uptime?

**Answer:**
- **Uptime** — raw time the service was up. 99.9% uptime = about 8.7 hours downtime per year.
- **Availability** — whether the service was usable when requested. A service could be "up" but returning errors. Availability is more meaningful.

SLA is usually expressed as availability. Example: 99.9% availability means at most 43 seconds downtime per month.

---

## SECTION 4: ACTIVE DIRECTORY

### Q20: What is Active Directory and how does it relate to monitoring?

**Answer:**
Active Directory is Microsoft's directory service. It stores users, computers, groups, and policies. It handles authentication and authorization.

In monitoring, I monitor AD by:
- Checking domain controller health (NTDS, DFS replication)
- Monitoring LDAP response times
- Alerting on account lockouts or failed logins
- Tracking replication latency between DCs
- Monitoring certificate expiry if AD CS is used

---

### Q21: What is LDAP and how is it used?

**Answer:**
LDAP is Lightweight Directory Access Protocol — the protocol used to query AD. Applications authenticate users by binding to LDAP. Port 389 (LDAP) or 636 (LDAPS).

In monitoring, some tools integrate with LDAP for user authentication and authorization. You can also monitor LDAP response times as a health check.

---

### Q22: What are FSMO roles?

**Answer:**
FSMO (Flexible Single Master Operation) roles are special roles in AD that only one DC can hold at a time. There are 5 roles:
1. Schema Master
2. Domain Naming Master
3. PDC Emulator (most important for monitoring — time sync)
4. RID Master
5. Infrastructure Master

If a DC holding these roles fails, AD functionality degrades. We monitor these for availability.

---

### Q23: How do you monitor AD replication?

**Answer:**
We check:
1. `repadmin /replsummary` — shows replication status across all DCs
2. Replication latency — time taken for changes to replicate
3. Tombstone lifetime — objects stay in tombstone for 60-180 days
4. USN (Update Sequence Number) gaps

Alerts when replication fails for more than 15 minutes or latency exceeds threshold.

---

## SECTION 5: AZURE

### Q24: What Azure services have you worked with?

**Answer:**
I have the AZ-900 certification. I've worked with:
- **Azure VMs** — provisioning, monitoring, NSG rules
- **Azure Networking** — VNet, subnets, NSG, peering
- **Azure Monitor** — metrics, logs, alerts, Application Insights
- **Azure Storage** — blob, disk, backup
- **Terraform on Azure** — IaC for VNet, NSG, VM deployment

---

### Q25: How does Azure Monitor work?

**Answer:**
Azure Monitor collects metrics and logs from Azure resources. It has:
- **Metrics** — numerical values (CPU %, disk IO, network in/out). Stored for 93 days.
- **Logs** — queryable using KQL. Stored in Log Analytics workspaces.
- **Alerts** — fire based on metric thresholds or log search results
- **Action groups** — define what happens when an alert fires (email, SMS, webhook, ITSM)
- **Workbooks** — interactive dashboards combining metrics and logs
- **Application Insights** — APM for applications (requests, exceptions, dependencies)

---

### Q26: How do you monitor Azure VMs?

**Answer:**
Enable Azure Monitor Agent on the VM. It collects:
- Guest OS metrics (CPU, memory, disk, network)
- Performance counters
- Event logs
- Syslog (Linux)

Set up alerts for high CPU > 90%, low disk space < 10%, or service failures. Optionally install Dependency Agent for mapping.

---

### Q27: What is Azure Log Analytics Workspace?

**Answer:**
It's the container where Azure logs are stored. Think of it as a database for logs. You write KQL queries to search, filter, and analyze logs. You can create alert rules based on query results. One workspace can collect logs from multiple Azure subscriptions and on-prem servers via Arc.

---

### Q28: What is Application Insights?

**Answer:**
It's Azure's APM (Application Performance Monitoring) tool. It monitors live web applications by instrumenting the code with an SDK. It captures:
- Request rates and response times
- Failure rates and exceptions
- Dependency calls (databases, APIs)
- Page views and load times (browser)
- Traces and logs

It pairs with Azure Monitor alerts. If error rate spikes, you get an alert and can drill into the specific failed request.

---

### Q29: What is Azure Arc?

**Answer:**
Azure Arc extends Azure management to on-premises and multi-cloud servers. You install the Azure Connected Machine agent on non-Azure servers, and they appear in Azure portal. You can then apply Azure Policy, install extensions, and monitor them with Azure Monitor — all without migrating to Azure.

---

## SECTION 6: SQL BACKUPS

### Q30: What is a SQL backup? Explain full, differential, and transaction log backups.

**Answer:**
- **Full backup** — copies the entire database. Large, takes time. Needed as a baseline.
- **Differential backup** — copies only data changed since last full backup. Smaller, faster.
- **Transaction log backup** — copies all transactions since last log backup. Small, frequent. Allows point-in-time recovery.

A typical strategy: Weekly full, daily differential, hourly log backups.

---

### Q31: What is RPO and RTO?

**Answer:**
- **RPO (Recovery Point Objective)** — how much data loss is acceptable. "If we lose data, how far back can we go?" RPO of 1 hour means log backups every hour.
- **RTO (Recovery Time Objective)** — how fast we need to recover. "If the server dies, how long until it's back?" RTO of 4 hours means we have 4 hours to restore.

Monitoring tracks: backup success/failure, RPO compliance, backup age.

---

### Q32: How do you monitor SQL backup success?

**Answer:**
Check:
1. SQL Server Agent job history (last run, success/failure)
2. MSDB database for backup history
3. Backup file existence and size
4. Restore verification (restore the backup to a test DB to confirm it works)
5. Alert if backup is older than RPO threshold

---

### Q33: What is a restore strategy vs backup strategy?

**Answer:**
Backup is only half the job. A restore strategy means:
1. Testing that backups actually work (restore to test environment)
2. Documenting the restore steps
3. Knowing the order: restore full, then latest differential, then all log backups since that diff
4. Measuring restore time to ensure it meets RTO

---

## SECTION 7: AUTOMATION & SCRIPTING

### Q34: What automation have you built in your current role?

**Answer:**
Three main things:

1. **Ansible auto-remediation** — When LM detects a critical alert, it triggers Ansible Tower via webhook. The playbook diagnoses and fixes the issue (restart service, clear disk space, restart process). Reduced manual incidents by 40%.

2. **Python + LM API** — Automated adding ping monitoring and service monitoring for new servers. Instead of manually configuring in UI, a Python script handles it via REST API.

3. **Ansible + LM API** — Dynamic IP updates. When server IPs change, Ansible playbook updates LM automatically.

---

### Q35: Explain how you built the Ansible auto-remediation workflow.

**Answer:**
LM alert fires → LM sends webhook to Ansible Tower → Ansible Tower runs the playbook matching the alert type → Playbook runs remediation (e.g., restart httpd service) → Ansible API sends acknowledgment back to LM → LM updates alert status.

I wrote the playbooks (restart services, disk cleanup, process health checks). The webhook payload included server hostname, alert message, and severity.

---

### Q36: What scripting languages do you know?

**Answer:**
- **Python** — most comfortable. Used for LM API integrations, data processing scripts. I know requests, json, csv, file I/O.
- **Bash/Shell** — Linux administration scripts, log parsing, cron jobs
- **Groovy** — used for LogicMonitor DataSource collection scripts. Basic level, used AI assistance.
- **PowerShell** — basic Windows administration

---

### Q37: Write a Python script to read a CSV of server IPs and ping each one.

**Answer:**
```python
import csv
import subprocess

with open("servers.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        ip = row[0]
        result = subprocess.run(["ping", "-c", "1", ip], capture_output=True)
        status = "UP" if result.returncode == 0 else "DOWN"
        print(f"{ip}: {status}")
```

---

### Q38: Write a Python script to make an API call and print the JSON response.

**Answer:**
```python
import requests
import json

url = "https://api.example.com/health"
headers = {"Authorization": "Bearer token123"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
```

---

### Q39: Explain exception handling in Python.

**Answer:**
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    print("Request timed out")
except requests.ConnectionError:
    print("Could not connect")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

### Q40: What is idempotency and why is it important in automation?

**Answer:**
Idempotency means running the same automation multiple times gives the same result. For example, an Ansible playbook that "ensures nginx is running" — if it's already running, the playbook does nothing. If it's stopped, it starts it.

Idempotency is important because automations run on schedules. Without it, scripts might cause unintended changes on every run.

---

## SECTION 8: KQL (Azure Analytics)

### Q41: What is KQL? Where do you use it?

**Answer:**
Kusto Query Language (KQL) is used to query Azure Monitor Logs, Application Insights, and Log Analytics. It's similar to SQL but optimized for large log datasets. Used in:
- Azure Log Analytics queries
- Application Insights search
- Azure Monitor alert rules
- Grafana dashboards with Azure data source

---

### Q42: Write a KQL query to find all 500 errors in the last 24 hours.

**Answer:**
```kql
requests
| where timestamp > ago(24h)
| where resultCode startswith "5"
| project timestamp, name, resultCode, url
| order by timestamp desc
```

---

### Q43: Write a KQL query to count errors by endpoint.

**Answer:**
```kql
requests
| where timestamp > ago(24h)
| where resultCode >= 400
| summarize ErrorCount = count() by url, resultCode
| order by ErrorCount desc
```

---

### Q44: Write a KQL query for server CPU over time.

**Answer:**
```kql
Perf
| where TimeGenerated > ago(6h)
| where CounterName == "% Processor Time"
| where ObjectName == "Processor"
| where InstanceName == "_Total"
| summarize AvgCPU = avg(CounterValue) by Computer, bin(TimeGenerated, 5m)
| render timechart
```

---

### Q45: Write a KQL query to find servers with low disk space.

**Answer:**
```kql
Perf
| where TimeGenerated > ago(1h)
| where CounterName == "% Free Space"
| where InstanceName matches regex "^[A-Z]:$"
| where CounterValue < 10
| project Computer, InstanceName, FreePercent = CounterValue, TimeGenerated
```

---

### Q46: What are KQL operators you commonly use?

**Answer:**
- `where` — filter rows
- `project` — select columns
- `summarize` — aggregate (count, avg, min, max, percentiles)
- `order by` / `sort by` — sort results
- `bin` — group by time buckets
- `render timechart` — visualize
- `join` — combine two tables
- `extend` — create new calculated columns
- `take` — limit results (like LIMIT in SQL)
- `ago()` — time filter (e.g., `ago(24h)`)

---

## SECTION 9: GENERAL MONITORING & OBSERVABILITY

### Q47: What is observability? How is it different from monitoring?

**Answer:**
Monitoring tells you if something is broken (known unknowns). Observability lets you understand WHY it broke by exploring unknown unknowns.

Monitoring answers: "Is the server up?"
Observability answers: "Why is the server responding slowly? Was it a code change? Network issue? DB contention?"

Observability is built on three pillars:
1. **Metrics** — numbers (CPU, latency, error rate)
2. **Logs** — events (error messages, debug output)
3. **Traces** — request flow across services

---

### Q48: What is the difference between a push and pull monitoring model?

**Answer:**
- **Pull** — monitoring server connects to the target and collects metrics (SNMP, Prometheus). Target doesn't know it's being monitored.
- **Push** — target sends metrics to the monitoring server (agent-based like LM collector). More firewall-friendly, target initiates.

LM uses a hybrid model — collectors are push-based to LM cloud, but the collector itself pulls data from targets via SNMP/WMI/script.

---

### Q49: Explain MTTR, MTBF, and MTTD.

**Answer:**
- **MTTR (Mean Time to Resolve)** — average time from alert to fix. Lower is better.
- **MTBF (Mean Time Between Failures)** — average uptime between incidents. Higher is better.
- **MTTD (Mean Time to Detect)** — average time from issue occurring to alert firing. Lower is better.

My Ansible auto-remediation reduced MTTR by 40% because playbooks started fixing issues immediately instead of waiting for human response.

---

### Q50: What is an SLA, SLO, and SLI?

**Answer:**
- **SLI (Service Level Indicator)** — what you measure. "Response time under 200ms."
- **SLO (Service Level Objective)** — your target. "99.9% of requests under 200ms."
- **SLA (Service Level Agreement)** — the contract. "If we miss 99.9%, you get a credit."

In monitoring, we track SLIs and alert when they're close to breaching SLO. For example: "Error rate is approaching the monthly SLO budget" fires a warning alert before actual breach.

---

### Q50b: What is OLA and how is it different from SLA?

**Answer:**
- **SLA (Service Level Agreement)** — agreement between the IT team and the customer/business. Defines what the user experiences. Example: "Application will be available 99.5% of the time."
- **OLA (Operational Level Agreement)** — internal agreement between IT teams. Example: "Infrastructure team will resolve network issues within 2 hours." It supports the SLA.

The SLA is the promise to the customer. The OLA is the internal agreement between teams that makes the SLA possible.

**Simple example:**
- SLA to business: "Password reset done within 1 hour"
- OLA between Service Desk and AD team: "AD team will resolve account unlock requests within 30 minutes"

As a monitoring engineer, my monitoring supports both: I track SLA compliance from the user side and measure OLA metrics between internal teams.

---

### Q50c: What is an UC (Underpinning Contract)?

**Answer:**
An UC is a contract with an **external** third-party supplier. If the SLA depends on a vendor (like an ISP or cloud provider), the UC is the legal agreement that ensures they meet their part.

- SLA = promise to customer
- OLA = agreement between internal teams
- UC = contract with external vendor

Example: If we host on Azure, we have an UC with Microsoft for 99.95% VM uptime. That UC feeds into our SLA calculations.

---

### Q50d: What is ITIL? What ITIL processes do you use in monitoring?

**Answer:**
ITIL is a framework of best practices for IT service management. It's not a tool — it's a set of processes.

The processes most relevant to my monitoring role:

| ITIL Process | How it applies to monitoring |
|---|---|
| **Incident Management** | Getting services back to normal ASAP. Alerts → incidents → resolution. My auto-remediation feeds directly into this. |
| **Problem Management** | Finding root cause of recurring incidents. Monitoring data (trends, patterns) helps identify underlying problems. |
| **Change Management** | Monitoring before and after changes to catch regressions. My LM dashboards show if a change degraded performance. |
| **Service Desk** | First point of contact. My monitoring alerts help them diagnose faster. |
| **Event Management** | THIS IS MY JOB. Monitoring detects events, filters them, and triggers appropriate responses. |
| **Availability Management** | Tracking uptime/SLA compliance. My monitoring generates availability reports. |
| **Capacity Management** | Monitoring trends to predict when we'll run out of resources. Proactive alerts before saturation. |
| **Service Continuity Management** | DR testing. Monitoring ensures failover works and DR sites are healthy. |

---

### Q50e: What is the Incident Management lifecycle?

**Answer:**
Standard ITIL incident lifecycle:

1. **Detection** — monitoring alerts or user reports a problem
2. **Logging** — incident created in ServiceNow with all details
3. **Categorization** — assign category (network, server, application, security)
4. **Prioritization** — based on impact (how many users) and urgency (how fast)
5. **Initial diagnosis** — L1 support checks runbook, tries known fixes
6. **Escalation** — if L1 can't fix, escalate to L2 (me) or L3 (engineering)
7. **Investigation and diagnosis** — deep dive using monitoring data, logs
8. **Resolution and recovery** — fix applied, service restored
9. **Incident closure** — ticket closed, user confirmed satisfied
10. **Post-incident review** — what went wrong, how to prevent recurrence

**My monitoring role touches steps 1, 4, 7, 8, and 10.**

---

### Q50f: What is a Major Incident? How do you handle it?

**Answer:**
A Major Incident is one with **high impact** (many users affected, revenue impact, security breach).

Process:
1. **Declare** — when criteria met (e.g., entire payment system down), declare major incident
2. **War room** — bring together all relevant teams (bridge call)
3. **Communicate** — regular updates to stakeholders every 30 minutes
4. **Fix** — focus on restoration, not root cause
5. **Resolve** — confirm service is back
6. **Post-mortem** — within 5 business days, write RCA (Root Cause Analysis) document

In monitoring, my job during a major incident is:
- Provide the war room with real-time dashboards
- Compare current state with before-incident baselines
- Check if related alerts fired and were missed
- After resolution, add preventive monitoring so we catch it earlier next time

---

### Q51: What is event correlation? How did you use BigPanda?

**Answer:**
Event correlation groups related alerts into a single incident. Without it, one server failure might generate 50 alerts (CPU, memory, disk, service down).

BigPanda uses machine learning to:
1. Deduplicate — remove identical alerts
2. Group — cluster related alerts by time and topology
3. Suppress — hide alerts from dependent resources

I configured BigPanda to ingest alerts from LM, correlate them into incidents, and route to the right team. This reduced alert noise significantly and helped the on-call team focus on real problems.

---

### Q52: Walk me through your on-call incident response process.

**Answer:**
1. **Alert fires** — LM detects threshold breach and sends to PagerDuty/BigPanda
2. **Acknowledge** — I acknowledge the alert within 5 minutes
3. **Diagnose** — Check dashboards, logs, and metrics. Is it a known issue? Runbook available?
4. **Fix or escalate** — If auto-remediation exists, check if playbook ran. If not, follow runbook steps. Escalate if needed.
5. **Resolve** — Fix the issue, verify monitoring shows green
6. **Post-mortem** — Was this a one-time blip or recurring? Should we add auto-remediation?

---

## SECTION 10: SCENARIO-BASED QUESTIONS

### Q53: You join as the only monitoring engineer. The team has 200 servers and no monitoring. What do you do?

**Answer:**
Phase 1 (Day 1-2): Set up basic availability monitoring for all 200 servers. Ping + SSH check. Identify the critical ones.

Phase 2 (Week 1): Add CPU, memory, disk monitoring for critical servers. Set up basic alert thresholds.

Phase 3 (Week 2): Add service-level monitoring for key applications. Check if specific processes are running.

Phase 4 (Week 3-4): Add API integrations with ticketing system. Set up on-call rotation with proper escalation. Create dashboards.

Phase 5 (Ongoing): Add synthetic monitoring for end users. Automate remediation for common issues. Refine alert thresholds.

---

### Q54: An important server goes down at 2 AM. Walk through your steps.

**Answer:**
1. Check if it's reachable (ping)
2. Check LM dashboard — was there any precursor (high CPU, memory leak)?
3. Check if auto-remediation playbook already ran
4. SSH into server (or check out-of-band management)
5. Check logs (application logs, system logs, dmesg)
6. Check resource usage during crash (OOM killer? disk full?)
7. Restart the service or server
8. Document what happened
9. Next day: root cause analysis and add preventive monitoring

---

### Q55: Your monitoring tool is generating too many false alerts. What do you do?

**Answer:**
1. Analyze the false alerts — what pattern do they share?
2. Adjust thresholds — maybe too sensitive
3. Add dependency awareness — don't alert on children when parent is down
4. Implement alert suppression during known maintenance windows
5. Use event correlation (BigPanda) to group related alerts
6. Tune per-service — some services need different thresholds
7. Monitor the monitor — track alert-to-ticket ratio and aim for >80% meaningful alerts

---

### Q56: A new service is being handed over to operations. What do you check?

**Answer:**
1. Monitoring — is it being monitored? CPU, memory, disk, application health?
2. Logs — are logs being collected and searchable?
3. Alerts — threshold-based alerts configured with right severity?
4. Runbook — documented for on-call team?
5. Backup — is data being backed up?
6. SLA — what's the expected availability?
7. Dependencies — does it depend on other services? Are those monitored too?
8. Dashboard — is there a service dashboard?
9. Escalation — who handles each alert level?

---

### Q57: What's an example of a difficult monitoring problem you solved?

**Answer:**
I had a case where a service would fail intermittently — maybe once every 2-3 days, but always recovered on restart. Standard monitoring showed nothing because by the time we checked, it was running fine.

I added a custom DataSource that collected application logs in real-time and checked for specific error patterns. I also added process-level metrics (memory handle count, thread count). This caught a memory leak that built up over 48 hours until the process crashed. We fixed the leak and added a preventive restart playbook as a temporary measure.

---

## QUICK REFERENCE CARDS (Print These)

### KQL Quick Reference
| Operator | Use |
|---|---|
| `where` | Filter rows |
| `project` | Pick columns |
| `summarize` | Aggregate |
| `ago(24h)` | Last 24 hours |
| `bin(time, 5m)` | Time buckets |
| `render timechart` | Graph |
| `order by` | Sort |
| `take 10` | Top 10 |

### Python Quick Reference
| Concept | Code |
|---|---|
| API call | `requests.get(url, headers=h)` |
| JSON parse | `data = response.json()` |
| JSON stringify | `json.dumps(payload)` |
| Read file | `open("file.txt").read()` |
| Loop | `for item in list:` |
| Error handling | `try: ... except: ...` |

### LM API Quick Reference
| Endpoint | Purpose |
|---|---|
| `GET /device/devices` | List devices |
| `POST /device/devices` | Add device |
| `POST /service/services` | Add service/ping monitor |
| `GET /alert/alerts` | List alerts |
| Auth header | `LMv1 {id}:{sig}:{epoch}` |

---
