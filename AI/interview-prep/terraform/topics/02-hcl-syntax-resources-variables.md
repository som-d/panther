# Topic 02: HCL Syntax, Resources, Variables, Data Sources

---

## 1. HCL Basics (HashiCorp Configuration Language)

HCL is Terraforms configuration language. Its declarative — you describe the desired end state, not the steps to get there.

### File Types
| Extension | Purpose | Auto-loaded? |
|-----------|---------|-------------|
| `.tf` | Configuration files | Yes |
| `.tfvars` | Variable values | Only with `-var-file` flag |
| `.tfstate` | State file (auto-generated) | N/A |
| `.terraform.lock.hcl` | Provider version lock file | Yes |

### Basic Structure

```hcl
# This is a comment

# Block type "label" "name" {
<BLOCK TYPE> "<LABEL>" "<NAME>" {
  # Arguments
  <ARGUMENT NAME> = <VALUE>
}
```

---

## 2. Core Blocks

### Provider Block
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}
```

**Key points:**
- Provider = the plugin that talks to Azure API
- `features {}` block allows provider-level configuration
- Version constraint `~> 4.0` means >= 4.0 and < 5.0
- `required_providers` is inside `terraform {}` block (MUST be at root level)

### Resource Block — THE most important block
```hcl
resource "azurerm_resource_group" "main" {
  name     = "myapp-rg"
  location = "eastus"
  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}
```

**Syntax:** `resource "<type>" "<local_name>" { ... }`
- **Type:** The Azure resource type (from provider docs)
- **Local name:** How you reference this resource in other blocks
- **Full address:** `azurerm_resource_group.main` (used in state commands)

### Variable Block
```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}
```

**Variable types:**
```hcl
variable "simple"    { type = string }
variable "number_ex" { type = number }
variable "bool_ex"   { type = bool }
variable "list_ex"   { type = list(string) }
variable "map_ex"    { type = map(string) }
variable "object_ex" {
  type = object({
    name    = string
    size    = string
    region  = string
  })
}
```

**Setting variable values (priority order, high to low):**
1. `-var` flag: `terraform apply -var="environment=prod"`
2. `-var-file` flag: `terraform apply -var-file="prod.tfvars"`
3. `terraform.tfvars` or `*.auto.tfvars` (auto-loaded)
4. Environment variable: `TF_VAR_environment=prod`
5. Default value

### Output Block
```hcl
output "resource_group_id" {
  value       = azurerm_resource_group.main.id
  description = "The ID of the resource group"
  sensitive   = false
}
```

**Outputs are used for:**
- Displaying useful information after apply
- Passing values between modules
- "Bridging" between different Terraform configurations

### Data Source Block
```hcl
data "azurerm_resource_group" "existing" {
  name = "production-rg"
}
```

**Data sources READ existing infrastructure — they do NOT create anything.**

Access: `data.azurerm_resource_group.existing.location`

**Common use cases:**
- Read existing resource group (instead of creating a new one)
- Get current Azure client config (`data "azurerm_client_config" "current" {}`)
- Fetch secrets from Key Vault

---

## 3. Referencing Resources and Attributes

```hcl
resource "azurerm_resource_group" "main" {
  name     = "myapp-rg"
  location = "eastus"
}

resource "azurerm_virtual_network" "main" {
  name                = "myapp-vnet"
  location            = azurerm_resource_group.main.location     # Attribute reference
  resource_group_name = azurerm_resource_group.main.name         # Attribute reference
  address_space       = ["10.0.0.0/16"]
}
```

**Pattern:** `<resource_type>.<local_name>.<attribute>`

**Implicit dependency:** When you reference one resource in another, Terraform automatically knows the order. Virtual network is created AFTER resource group.

**Explicit dependency (rarely needed):**
```hcl
depends_on = [
  azurerm_resource_group.main
]
```
Use only when Terraform cant infer the dependency (e.g., when using `data` sources or module outputs).

---

## 4. Terraform Expressions

### String Interpolation
```hcl
name = "myapp-${var.environment}"
  # If var.environment = "prod" -> "myapp-prod"
```

### Conditionals
```hcl
vm_size = var.environment == "prod" ? "Standard_D4s_v3" : "Standard_B2s"
```

### Functions
```hcl
# String functions
lower("PROD")          -> "prod"
upper("prod")          -> "PROD"
format("%s-%s", "app", "prod") -> "app-prod"

# Collection functions
concat(["a", "b"], ["c"]) -> ["a", "b", "c"]
length(["a", "b", "c"])   -> 3
lookup({a=1, b=2}, "a")   -> 1

# File functions
file("${path.module}/template.yaml")
templatefile("${path.module}/cloud-init.tpl", {
  hostname = "myapp-server"
})
```

### for_each and count (Creating Multiple Resources)

**count** — create N copies:
```hcl
variable "subnet_names" {
  default = ["subnet-a", "subnet-b", "subnet-c"]
}

resource "azurerm_subnet" "main" {
  count                = length(var.subnet_names)
  name                 = var.subnet_names[count.index]
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.${count.index}.0/24"]
}
```

**for_each** — create from map or set:
```hcl
variable "subnets" {
  default = {
    "subnet-a" = "10.0.1.0/24"
    "subnet-b" = "10.0.2.0/24"
    "subnet-c" = "10.0.3.0/24"
  }
}

resource "azurerm_subnet" "main" {
  for_each             = var.subnets
  name                 = each.key
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [each.value]
}
```

**When to use which:**
| count | for_each |
|-------|----------|
| Fixed number of resources | Dynamic set based on data |
| Resources indexed by number | Resources keyed by unique key |
| Changes can shift indexes | Changes only affect specific key |
| Simpler syntax | Safer for evolving infrastructure |

---

## 5. Locals

Locals are evaluated expressions that you can reference multiple times:
```hcl
locals {
  project     = "myapp"
  environment = var.environment
  name_prefix = "${local.project}-${local.environment}"

  common_tags = {
    Project     = local.project
    Environment = local.environment
    ManagedBy   = "Terraform"
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}
```

**Why use locals:**
- Avoid repeating complex expressions
- Single place to change naming conventions
- More readable than inline expressions

---

## 6. Complete Example: Deploy a VM (Interview-Ready)

```hcl
# main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Invalid environment"
  }
}

variable "vm_size" {
  description = "VM SKU"
  type        = string
  default     = "Standard_B2s"
}

# Locals
locals {
  name_prefix = "myapp-${var.environment}"
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Resources
resource "azurerm_resource_group" "main" {
  name     = "${local.name_prefix}-rg"
  location = "eastus"
  tags     = local.common_tags
}

resource "azurerm_virtual_network" "main" {
  name                = "${local.name_prefix}-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_subnet" "main" {
  name                 = "${local.name_prefix}-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_public_ip" "main" {
  name                = "${local.name_prefix}-pip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = local.common_tags
}

resource "azurerm_network_interface" "main" {
  name                = "${local.name_prefix}-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

resource "azurerm_linux_virtual_machine" "main" {
  name                  = "${local.name_prefix}-vm"
  location              = azurerm_resource_group.main.location
  resource_group_name   = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.main.id]
  size                  = var.vm_size

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  computer_name                   = "${local.name_prefix}-vm"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }

  tags = local.common_tags
}

# Outputs
output "public_ip" {
  value       = azurerm_public_ip.main.ip_address
  description = "VM public IP address"
}

output "vm_id" {
  value       = azurerm_linux_virtual_machine.main.id
  description = "VM resource ID"
}
```

---

## Interview Questions This Topic Covers

**Q: "What is the difference between a resource and a data source?"**
A: Resources CREATE/MANAGE infrastructure. Data sources READ existing infrastructure. Resources can be created, updated, or destroyed. Data sources are read-only.

**Q: "How does Terraform know the order to create resources?"**
A: It builds a DAG (Directed Acyclic Graph) from implicit dependencies (attribute references between resources). It creates resources that have no dependencies first, then resources that depend on them, etc.

**Q: "Explain count vs for_each"**
A: Count creates indexed resources (0, 1, 2...). Changing the middle shifts all subsequent indexes. For_each creates keyed resources from a map/set. Changes only affect the specific key — safer for evolving infrastructure.

**Q: "What are locals used for?"**
A: Locals are evaluated expressions that avoid repetition. They reduce hardcoding and centralize naming, tagging, and configuration logic.

---

## Key Takeaways

```
HCL = Declarative language
Resources = CREATE infrastructure
Data Sources = READ infrastructure  
Variables = Input parameters
Outputs = Return values
Locals = Internal derived values
```

**Practice:**
1. Write a .tf file with a resource group, VNet, and subnet
2. Add variables for environment, location, and CIDR
3. Use locals for consistent naming and tagging
4. Add outputs for the VNet and subnet IDs
5. Run `terraform plan` to verify

---

*Next: 03-modules.md*
