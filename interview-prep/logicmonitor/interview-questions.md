# LogicMonitor Interview Questions (7-14 LPA)

**Note:** You use LogicMonitor DAILY. These questions test if you can EXPLAIN monitoring well.

---

### Q1: "What monitoring tools have you used?"

> "I use LogicMonitor at Wipro for Azure infrastructure monitoring. It's an enterprise SaaS platform. I manage monitoring for 50+ Azure VMs, configure custom alert thresholds, build service dashboards, and handle incident response."
>
> **Why this wins:** You don't just name a tool — you describe HOW you use it. Shows real experience.

---

### Q2: "How do you decide what to alert on?"

> "I follow the RED method for services: Rate (requests/second), Errors (failure percentage), Duration (latency p95). For infrastructure, I use the USE method: Utilization, Saturation, Errors. I alert on SYMPTOMS (error rate > 5%) not causes (CPU > 80%). In LogicMonitor, I use dynamic thresholds so the system learns normal behavior and only alerts on anomalies."

---

### Q3: "How do you handle alert fatigue?"

> "At Wipro, we had too many static thresholds causing false alarms. I moved to LogicMonitor's dynamic thresholding — it baselines over 2-4 weeks and alerts only on anomalies. We also implemented escalation policies (email -> Slack -> SMS -> PagerDuty) so the same alert doesn't fire repeatedly. Alert fatigue dropped by 60%."

---

### Q4: "LogicMonitor vs Prometheus — compare them"

> "LogicMonitor is SaaS (zero maintenance, 2000+ integrations, built-in dashboards). Prometheus is self-hosted (more flexible, pull-based architecture, needs Grafana + Alertmanager). If I joined a Prometheus shop, I'd adapt quickly — the monitoring concepts are identical, just different syntax."

---

### Q5: "What metrics do you monitor for a web application?"

> "Using the RED method:
> - Request rate (RPS)
> - Error rate (5xx percentage)
> - Latency (p50 for user experience, p95 for outliers, p99 for worst-case)
> - Active users / sessions
>
> Plus infrastructure: CPU, memory, disk, network. I organize these into a single dashboard so when an alert fires, I can see all relevant metrics at once."

---

### Q6: "Walk me through how you debug a production issue"

> "1. Alert fires in LogicMonitor (e.g., error rate spike)
> 2. Check the service dashboard — see latency graph, error rate, RPS
> 3. Check infrastructure metrics — CPU/memory on affected servers
> 4. Check deployment timeline — was there a recent deploy?
> 5. Check logs for error patterns
> 6. Identify root cause, rollback or hotfix
> 7. Verify fix in LogicMonitor — metrics return to baseline
> 8. Post-mortem document"

---

### Q7: "How does monitoring fit into DevOps?"

> "Monitoring closes the feedback loop. CI/CD deploys code, monitoring tells you if the deploy was successful. Without monitoring, you're deploying blind. I set up alerts for key metrics BEFORE a deploy, so if error rate spikes, we rollback automatically."

---

## Key Phrases to Use

| Topic | Say This |
|-------|----------|
| Your LM experience | "50+ Azure VMs, dynamic thresholds, service dashboards, incident response" |
| Alerting philosophy | "Alert on symptoms, not causes. Dynamic thresholds, not static." |
| Monitoring methodology | "RED method for services, USE method for infrastructure" |
| Adaptability | "I could pick up Prometheus/Datadog in a week — concepts are the same" |
| Incident response | "Detect -> Acknowledge -> Assess -> Mitigate -> Resolve -> Post-mortem" |
