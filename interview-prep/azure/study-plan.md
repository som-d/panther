# Azure Interview Study Plan

**Target Level:** Mid-level DevOps (3+ YOE) | 7-14 LPA interviews
**Context:** You already work with Azure daily at Wipro — this focuses on gaps and interview-level depth
**Key Rule:** Dont study what you already know. Study what product companies ask that you havent been exposed to.

---

## What You Already Know (From Wipro)

- Azure Portal navigation
- Creating VMs, resource groups, storage accounts
- Basic networking (VNet, NSG rules)
- Azure Monitor basics (alerts, metrics)

## What Product Companies Ask That You Need To Learn

---

## Week 3: Azure Networking Deep Dive

### Day 1: VNet Architecture (TOPIC 01)
- VNet address space design (CIDR notation)
- Subnets: public vs private, sizing (how big should each subnet be?)
- VNet peering (connect VNets across regions)
- **Interview angle:** "Design a VNet for a 3-tier application"
  - Web subnet /24, App subnet /24, DB subnet /24, GatewaySubnet /27
  - NSG per subnet with least-privilege rules

### Day 2: Network Security + Connectivity (TOPIC 02)
- NSG rules: priority, source/destination, protocol, port
- ASG (Application Security Groups) vs NSG
- Azure Firewall vs NSG (when to use which)
- Load Balancer (Azure LB): public vs internal, SKU comparison
- Application Gateway: layer 7 routing, WAF, SSL termination
- **Key difference:** Azure LB is layer 4, App Gateway is layer 7

### Day 3: DNS + Private Connectivity (TOPIC 03)
- Azure DNS: zones, records, private DNS zones
- Private Link / Private Endpoint — secure access to Azure PaaS without public internet
- Azure Bastion — secure VM access without public IP
- **Interview question:** "How do you connect an on-prem network to Azure?" (Answer: VPN Gateway or ExpressRoute)

### Day 4: Azure Compute (TOPIC 04)
- VM series: General purpose (D-series), Compute optimized (F-series), Memory optimized (E-series)
- VMSS (Virtual Machine Scale Sets) — auto-scaling, load balancing
- Availability Sets vs Availability Zones vs Scale Sets
- **Interview trap:** "Tell me about a time a VM went down" — talk about Availability Zones (99.99% SLA) vs Sets (99.95%)

### Day 5: Azure Storage (TOPIC 05)
- Storage types: Blob, Disk, File, Queue, Table
- Storage account types: Standard vs Premium, LRS vs GRS vs ZRS
- Blob tiers: Hot, Cool, Archive
- Managed Disks: SSD vs HDD, disk bursting
- Shared Access Signatures (SAS) — secure temporary access tokens

### Day 6: Identity + Access Management (TOPIC 06)
- Azure RBAC: built-in roles (Contributor, Owner, Reader), custom roles
- Managed Identity — the RIGHT way to give VMs/apps access to Azure resources
- Service Principal vs Managed Identity
- Azure AD basics: what it is, how it differs from Active Directory (on-prem)
- Key Vault: secrets, keys, certificates. Access policies vs RBAC

### Day 7: Azure Monitor + Logging (TOPIC 07)
- Azure Monitor: metrics, logs, alerts
- Log Analytics Workspace: KQL basics (just the syntax, 10-15 min)
- Diagnostic settings: where to send logs (Storage, Event Hub, Log Analytics)
- **Practical:** "How do you debug why a VM is unhealthy?"
  - Check Metrics -> CPU/Memory -> Check Activity Log -> Check Azure Monitor alerts -> Check NSG flow logs

---

## Week 4: AKS + Containers + Advanced

### Day 8: AKS Fundamentals (TOPIC 08)
- What is AKS? (Managed Kubernetes on Azure)
- Node pools: system vs user, scaling
- Pods, Deployments, Services (ClusterIP, NodePort, LoadBalancer)
- **Key insight:** You dont need to be a K8s expert. Just understand how AKS fits into DevOps workflows.
- AKS + Terraform: creating AKS cluster with azurerm_kubernetes_cluster

### Day 9: ACR + Container Registry (TOPIC 09)
- ACR (Azure Container Registry): store Docker images
- ACR Tasks: build images in Azure (no local Docker needed)
- Integration with AKS: AKS pulls images from ACR
- Geo-replication for multi-region deployments

### Day 10: Azure DevOps Integration (covered in azure-devops/ folder)
- Only study what directly relates to Azure services

### Day 11: Backup + Disaster Recovery (TOPIC 10)
- Azure Backup: VM backup, fileshare backup
- Site Recovery: DR to secondary region
- Snapshots: disk snapshots for quick restore
- **Interview scenario:** "Our prod DB is in Azure. How do we ensure DR?"
  - Primary region is eastus, DR in westus. Use Azure Site Recovery for VMs, Geo-redundant storage for DB, Traffic Manager for DNS failover.

### Day 12: Cost Management + Tagging (TOPIC 11)
- Azure Cost Management: budgets, alerts, recommendations
- Resource tagging strategy: Environment, Application, Owner, CostCenter
- **Why product companies care:** Cost optimization is a MAJOR part of DevOps in product companies. Every interviewer will ask about cost management.
- Azure Reservations vs Pay-as-you-go

### Day 13-14: Practice — Build and Present

**Exercise:** Design and present an Azure infrastructure for a product company:

```
Requirements:
- Web app with auto-scaling (3-10 instances)
- PostgreSQL database
- Redis cache
- Private networking (no public access to DB/cache)
- CI/CD integration
- Monitoring + alerting
- Budget: $1000/month (dev), $5000/month (prod)

Your design:
- Resource group per environment (dev-rg, prod-rg)
- VNet /16 with subnets: web /24, app /24, data /24
- VMSS for web tier
- Azure Database for PostgreSQL (private endpoint)
- Azure Cache for Redis (private endpoint)
- Azure Load Balancer + App Gateway (WAF enabled)
- Azure Monitor + Log Analytics
- Tag everything: Environment, Application, CostCenter
```

---

## Interview Depth Guide

| Topic | Must Know | Nice to Know | Dont Bother |
|-------|-----------|-------------|-------------|
| VNet/Subnet | CIDR, NSG, peering, address space design | VNet flow logs, service endpoints | VNet injection, Azure DNS Private Resolver |
| Compute | VM series, VMSS, availability options | Proximity placement groups, dedicated hosts | Azure Batch, Azure Spring Apps |
| Storage | Blob tiers, account types, SAS tokens | Immutable storage, object replication | Azure NetApp Files, Azure HPC Cache |
| RBAC | Built-in roles, Managed Identity, Service Principal | Custom roles, PIM, Azure AD B2C | Azure AD Connect sync |
| AKS | What it is, node pools, basic pods/services | Ingress controller, Helm charts | Service mesh (Istio), K8s operators |
| Monitor | Metrics, logs, alerts, Log Analytics | KQL queries (basic), workbooks | Application Insights deep dive |

---

## Common Interview Questions

1. "Whats the difference between Azure LB and Application Gateway?"
2. "How do you secure a VNet?"
3. "Explain Managed Identity vs Service Principal"
4. "What storage tier would you use for: logs (7 day retention), backups (1 year), archives (7 years)?"
5. "How do you handle cost optimization in Azure?"
6. "Design networking for a multi-tier app"
7. "Whats the difference between an NSG and Azure Firewall?"
8. "How do you give a VM access to Key Vault?" (Answer: Managed Identity)
9. "What happens when a VMSS scale-out triggers?"
10. "Explain Azure Backup vs Site Recovery"

---

## Quick Azure Facts for Interviews

| Fact | Why It Matters |
|------|---------------|
| Azure has 60+ regions worldwide (more than AWS/GCP) | Shows global scale awareness |
| Availability Zones = physical separation within a region | 99.99% SLA |
| Managed Identity = no credentials in code | Security best practice |
| Tags = cost allocation | Product companies budget by team |
| Private Endpoint = PaaS without public internet | Security compliance |

---

*Last updated: 21 May 2026 | Next: topics/01-vnet-architecture.md*
