# LogicMonitor Interview Study Plan

**Target:** DevOps Engineer, 3+ YOE | 7-14 LPA interviews
**Context:** You use LogicMonitor DAILY at Wipro. This is about interview ARTICULATION.
**Goal:** Turn your daily LM usage into a compelling monitoring story for product companies.

---

## Why LogicMonitor Matters in Interviews

Product companies will ask about monitoring. Since you use LogicMonitor:

1. **You have REAL monitoring experience** — most candidates only know theory
2. **You understand alerts, dashboards, and incident response** — every product company needs this
3. **You can compare LM with other tools** — shows breadth

**Key angle:** Frame LogicMonitor as your "monitoring foundation" — you know monitoring concepts, and picking up Prometheus/Grafana/Datadog is just syntax.

---

## Interview Gap Analysis (What You Know vs What They Ask)

| You Know (Wipro) | Interviewers Want To Hear |
|-----------------|--------------------------|
| Creating alerts in LM | HOW you designed the alerting strategy (severity, thresholds, escalation) |
| Building dashboards | WHAT metrics you track and WHY (RED method, USE method) |
| Managing 50+ devices | How you SCALE monitoring to 500+ devices |
| Responding to alerts | Your INCIDENT RESPONSE process |
| LM specific features | How you'd achieve the SAME thing with Prometheus/Datadog |

---

## 1. Core Monitoring Concepts (You Know These, Articulate Them)

### The RED Method (Say This in Interviews)
> "I follow the RED method for monitoring: Rate (requests/second), Errors (failure count/percentage), Duration (latency p50/p95/p99). This gives me the three most important signals for any service."

### The USE Method (For Infrastructure)
> "For infrastructure monitoring, I use the USE method: Utilization (how busy?), Saturation (is there queueing?), Errors (are things failing?). CPU, memory, disk, network — each checked for U, S, E."

### Four Golden Signals (Google SRE)
> Request Rate, Error Rate, Latency, Saturation. Google SRE book — mentioning it shows depth.

---

## 2. LogicMonitor-Specific Interview Answers

### Q: "What monitoring tool do you use?"
> "I use LogicMonitor at Wipro. It's a SaaS-based monitoring platform that supports 2000+ integrations across cloud, on-prem, and hybrid environments. I manage monitoring for 50+ devices including Azure VMs, on-prem servers, and network equipment."

### Q: "How do you set up alerting?"
> "In LogicMonitor, I follow a tiered alerting strategy:
> - **Critical (P1):** Service down, data loss → SMS + phone call, 5-min response
> - **Warning (P2):** High error rate, disk > 90% → Email + Slack, 30-min response
> - **Info (P3):** Cert expiry, patch due → Dashboard only
>
> I use dynamic thresholds where LM learns normal behavior and alerts only on anomalies. This reduces alert fatigue significantly."

### Q: "How do you handle alert fatigue?"
> "At Wipro, we initially had too many static thresholds causing false alarms. I moved to LogicMonitor's dynamic thresholding — it baselines metrics over 2-4 weeks and only alerts on actual anomalies. We also implemented escalation policies so the same alert doesn't fire multiple times. Alert fatigue dropped by 60%."

### Q: "What metrics do you monitor for Azure?"
> "Using LogicMonitor's Azure integration:
> - VM: CPU, memory, disk IOPS, network throughput
> - Azure SQL: DTU consumption, deadlocks, connection pool
> - Storage: latency, availability, egress
> - AKS: node/pod health, resource utilization
>
> I organize these into service-specific dashboards: one for web tier, one for database, one for infrastructure."

### Q: "How does LogicMonitor compare to Prometheus?"
| Aspect | LogicMonitor | Prometheus |
|--------|-------------|------------|
| Setup | SaaS — zero infrastructure | Self-hosted (server, storage, maintenance) |
| Integrations | 2000+ built-in | Custom exporters needed |
| Alerting | Built-in with escalation | Requires Alertmanager |
| Dashboards | Built-in | Requires Grafana |
| Scaling | Managed | You manage |

> "I use LogicMonitor daily. If I joined a company using Prometheus, I'd adapt quickly because the monitoring concepts are the same — metrics collection, alert rules, dashboard visualization. The tool is just syntax."

---

## 3. LogicMonitor Concepts to Highlight

### Key LM Features to Mention:
- **Dynamic thresholds** — ML-based baselining
- **Auto-discovery** — automatically detects new devices/resources
- **2000+ integrations** — Azure, AWS, GCP, Docker, Kubernetes
- **NOC dashboards** — real-time service health views
- **Alert escalation** — email -> SMS -> phone -> PagerDuty
- **Log monitoring** — centralized log management
- **Website monitoring** — external HTTP checks

### How to Frame Your LM Experience:
> "At Wipro, I manage monitoring for our client's Azure infrastructure using LogicMonitor. I've configured:
> - Custom alert thresholds for 50+ Azure VMs
> - Service-level dashboards for web, app, and database tiers
> - Escalation policies integrated with Slack and email
> - Auto-discovery for new resources (no manual setup)
>
> This gives me production experience with enterprise monitoring that most junior candidates lack."

---

## 4. Monitoring Interview Questions (General + LM Angle)

### Q1: "What's the difference between monitoring and observability?"
> **Monitoring** is knowing what to check (predefined alerts + dashboards).
> **Observability** is being able to explore unknown failure modes (metrics + logs + traces).
> 
> LogicMonitor handles monitoring well. For observability, you'd add distributed tracing (Jaeger) and structured logging (ELK).

### Q2: "How do you debug a slow web application?"
> 1. Check LM dashboard for latency spikes (p95, p99)
> 2. Check CPU/memory on web servers
> 3. Check database query performance
> 4. Check network latency between tiers
> 5. Check for recent deployments or config changes
> 6. Use logs to find error patterns

### Q3: "How would you monitor a newly deployed microservice?"
> 1. Expose /metrics endpoint (Prometheus format)
> 2. Add to LogicMonitor via custom integration or push to LM collector
> 3. Configure RED method alerts (Rate, Errors, Duration)
> 4. Create service dashboard
> 5. Set up escalation policy
> 6. Test alert with actual failure scenario

### Q4: "What's your incident response process?"
> 1. **Detect:** Alert fires in LogicMonitor
> 2. **Acknowledge:** Respond in Slack/PagerDuty within 5 min (P1)
> 3. **Assess:** Check dashboard + logs for root cause
> 4. **Mitigate:** Rollback, scale up, or apply hotfix
> 5. **Resolve:** Confirm fix, close alert
> 6. **Post-mortem:** Document what happened, why, and how to prevent

---

## 5. Key Interview Phrases

| Phrase | When to Say It |
|--------|---------------|
| "I use LogicMonitor at Wipro for Azure monitoring — dynamic thresholds, auto-discovery, 2000+ integrations" | "What monitoring tools have you used?" |
| "I follow the RED method: Rate, Errors, Duration" | "How do you monitor services?" |
| "Alert fatigue is real — we reduced it 60% with dynamic thresholds" | "How do you handle alerting?" |
| "Monitoring tells you what's broken, observability tells you WHY" | "Monitoring vs observability?" |
| "I could pick up Prometheus quickly — the concepts are the same" | "We use Prometheus here, can you adapt?" |

---

## 6. Quick Reference

```
YOUR MONITORING STORY (30-second version):
"I manage Azure monitoring with LogicMonitor at Wipro — 
50+ VMs, custom dashboards, dynamic threshold alerts, 
Slack integration. I follow the RED method for service monitoring 
and the USE method for infrastructure. If I joined a company 
using Prometheus/Datadog, the concepts transfer directly."

KEY METRICS YOU TRACK:
┌────────────┬───────────────┬──────────────────┐
│ Service    │ RED Metrics   │ Threshold         │
├────────────┼───────────────┼──────────────────┤
│ Web tier   │ RPS, 5xx, p95 │ Error > 1%        │
│ App tier   │ RPS, latency  │ Latency > 500ms   │
│ Database   │ Connections   │ Connections > 80% │
│ Infra      │ CPU, Memory   │ CPU > 90% 5min    │
└────────────┴───────────────┴──────────────────┘
```

---

*Next: interview-questions.md for focused practice*
