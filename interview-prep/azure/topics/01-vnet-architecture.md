# Topic 01: Azure VNet Architecture

**Why This Matters:** VNet design is the #1 Azure interview topic. Every product company interviewer will ask you to design a network. Your answer separates "portal user" from "architect."

---

## 1. VNet Basics

A Virtual Network (VNet) is Azure's isolated network. Think of it as your own private data center in the cloud.

**Key properties:**
- **Address space:** One or more CIDR ranges (e.g., 10.0.0.0/16)
- **Region-scoped:** A VNet lives in ONE Azure region
- **Isolated by default:** VNets cant talk to each other without peering
- **Subscription-scoped:** VNet is inside a resource group, which is inside a subscription

```hcl
resource "azurerm_virtual_network" "main" {
  name                = "myapp-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]

  tags = {
    Environment = "Production"
  }
}
```

---

## 2. CIDR Cheat Sheet (You MUST Know This)

| CIDR | Netmask | Usable IPs | Use Case |
|------|---------|-----------|----------|
| /16 | 255.255.0.0 | 65,536 | Entire VNet |
| /24 | 255.255.255.0 | 256 | Single subnet (most common) |
| /25 | 255.255.255.128 | 128 | Small subnet |
| /26 | 255.255.255.192 | 64 | Tiny subnet |
| /27 | 255.255.255.224 | 32 | GatewaySubnet |
| /28 | 255.255.255.240 | 16 | Azure Firewall subnet |

**Azure reserves 5 IPs per subnet** (first 4 + last 1). So a /24 has 251 usable IPs, not 256.

---

## 3. Subnet Design for a 3-Tier Application

**Scenario:** Design a VNet for a typical product company web application.

```
VNet: 10.0.0.0/16 (65,536 IPs)

Subnets:
  snet-web       10.0.1.0/24  (251 IPs)  - Web servers / VMSS
  snet-app       10.0.2.0/24  (251 IPs)  - Application servers
  snet-data      10.0.3.0/24  (251 IPs)  - Databases
  snet-gateway   10.0.4.0/27  (27 IPs)   - VPN Gateway
  snet-bastion   10.0.4.32/27 (27 IPs)   - Azure Bastion
  snet-firewall  10.0.4.64/26 (61 IPs)   - Azure Firewall
  snet-private   10.0.5.0/24  (251 IPs)  - Private Endpoints
```

**Rules:**
- Web subnet: inbound from internet (80/443 via App Gateway), outbound to app subnet
- App subnet: inbound from web subnet only, outbound to data subnet
- Data subnet: inbound from app subnet only (1433 for SQL, 3306 for MySQL, 6379 for Redis)
- Gateway/Bastion/Firewall: dedicated subnets with /27 minimum

---

## 4. NSG (Network Security Group)

An NSG is a stateful firewall attached to a subnet or NIC.

```hcl
resource "azurerm_network_security_group" "web_subnet" {
  name                = "nsg-web-subnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "AllowHTTPInbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefixes    = ["Internet"]
    destination_address_prefix = "VirtualNetwork"
  }

  security_rule {
    name                       = "DenyAllInbound"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefixes    = ["*"]
    destination_address_prefix = "*"
  }
}
```

**Priority rules:**
- Lower number = higher priority
- Processed in order (100, 101, 102...)
- Last rule is always "Deny All" (implicit)
- Azure default rules (AllowVNetInBound, AllowAzureLoadBalancerInBound) have priority 65000+
- Your custom rules (100-4096) take precedence over defaults

**Interview tip:** When asked "How would you secure a subnet?", answer with NSG rules + ASGs:

```hcl
# Application Security Groups (logical grouping, not IP-based)
resource "azurerm_application_security_group" "web" {
  name                = "asg-web"
  location            = ...
  resource_group_name = ...
}
resource "azurerm_application_security_group" "app" {
  name                = "asg-app"
  location            = ...
  resource_group_name = ...
}

# Reference ASGs in NSG rules (cleaner than IP ranges)
security_rule {
  name                                  = "AllowWebToApp"
  priority                              = 200
  direction                             = "Inbound"
  access                                = "Allow"
  protocol                              = "Tcp"
  source_port_range                     = "*"
  destination_port_range                = "8080"
  source_application_security_group_ids = [azurerm_application_security_group.web.id]
  destination_application_security_group_ids = [azurerm_application_security_group.app.id]
}
```

---

## 5. VNet Peering

Connects two VNets so they can communicate as if they were one network.

```hcl
resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  name                         = "hub-to-spoke"
  resource_group_name          = azurerm_resource_group.hub.name
  virtual_network_name         = azurerm_virtual_network.hub.name
  remote_virtual_network_id    = azurerm_virtual_network.spoke.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = false  # Hub firewall handles inspection
}

resource "azurerm_virtual_network_peering" "spoke_to_hub" {
  name                         = "spoke-to-hub"
  resource_group_name          = azurerm_resource_group.spoke.name
  virtual_network_name         = azurerm_virtual_network.spoke.name
  remote_virtual_network_id    = azurerm_virtual_network.hub.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true   # Send traffic through hub
}
```

**Types of peering:**
- **Regional:** Same region — free data transfer inbound
- **Global:** Different regions — small cost
- **Transit:** Not supported directly (VNet peering is NOT transitive). Use Azure Firewall or VPN Gateway for transit routing.

**Interview pattern:** Hub-spoke architecture
- Hub VNet: shared services (firewall, VPN gateway, monitoring)
- Spoke VNets: each application (dev, staging, prod)
- Peering between hub and each spoke
- All traffic flows through hub firewall

---

## 6. Azure Load Balancer

Layer 4 (TCP/UDP) load balancing. Distributes traffic to backend pool.

```hcl
resource "azurerm_lb" "main" {
  name                = "lb-web"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"  # Required for availability zones

  frontend_ip_configuration {
    name                 = "public-ip"
    public_ip_address_id = azurerm_public_ip.lb.id
  }
}

resource "azurerm_lb_backend_address_pool" "main" {
  name            = "backend-pool"
  loadbalancer_id = azurerm_lb.main.id
}

resource "azurerm_lb_probe" "main" {
  name            = "health-probe"
  loadbalancer_id = azurerm_lb.main.id
  protocol        = "Tcp"
  port            = 80
  interval        = 5    # seconds
  number_of_probes = 2   # unhealthy after 2 failures
}

resource "azurerm_lb_rule" "main" {
  name                           = "http-rule"
  loadbalancer_id                = azurerm_lb.main.id
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "public-ip"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.main.id]
  probe_id                       = azurerm_lb_probe.main.id
}
```

**Load Balancer vs Application Gateway:**

| Feature | Azure LB (Layer 4) | App Gateway (Layer 7) |
|---------|-------------------|----------------------|
| Protocol | TCP/UDP | HTTP/HTTPS |
| Routing | By source IP | By URL path, host header |
| SSL termination | No | Yes |
| WAF | No | Yes (OWASP rules) |
| Session affinity | Source IP | Cookie-based |
| When to use | Any TCP/UDP traffic | Web applications with routing needs |

---

## 7. Quick Interview Design Exercise

**Problem:** "Design a VNet for a production application that needs:
- Web tier (auto-scaling)
- API tier
- Database tier (PostgreSQL)
- Redis cache
- All traffic inspected by firewall
- No public access to API/DB/Redis"

**Solution:**
```
VNet: 10.0.0.0/16
  - snet-web:      10.0.1.0/24  -> App Gateway (public) -> VMSS web
  - snet-api:      10.0.2.0/24  -> Internal LB -> API servers  
  - snet-data:     10.0.3.0/24  -> Private endpoints for PostgreSQL + Redis
  - snet-firewall: 10.0.4.0/26  -> Azure Firewall

Security:
  - NSG on web: allow 80/443 from Internet, allow to API subnet
  - NSG on api: allow from web subnet only
  - NSG on data: allow from api subnet only (on database ports)
  - Azure Firewall: inspect all traffic between subnets
  - Private Endpoints for PostgreSQL + Redis (no public IP)
```

---

## Key Takeaways

```
VNet design interview cheat sheet:
1. CIDR /16 for VNet, /24 for subnets
2. Always plan for growth (dont use /24 for everything)
3. NSG per subnet with least-privilege rules
4. ASG for logical grouping (better than IP ranges)
5. Hub-spoke for multi-app environments
6. App Gateway for web, Azure LB for internal
7. Private Endpoint for PaaS services
8. Azure Firewall for traffic inspection
```

---

*Next: 02-network-security-connectivity.md*
