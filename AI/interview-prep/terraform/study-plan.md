# Terraform Interview Study Plan

**Target Level:** Mid-level DevOps (3+ YOE) | 7-14 LPA interviews
**Focus:** What Indian product companies actually ask
**Prerequisite:** You already know Ansible — do NOT confuse Terraform with config management

---

## Core Mindset Shift: Ansible vs Terraform

| Aspect | Ansible (what you know) | Terraform (what to learn) |
|--------|------------------------|--------------------------|
| Category | Config management | Infrastructure provisioning |
| State | Stateless (runs every time) | Stateful (tracks real world) |
| Language | YAML (declarative playbooks) | HCL (declarative + some logic) |
| Idempotency | By module design | Built-in via state comparison |
| Drift detection | Manual or periodic | Built-in via `terraform plan` |
| Best for | Configuring existing servers | Creating/managing infra resources |

**Interview tip:** When asked "Why Terraform over Ansible?", say:
> "Terraform is for provisioning infrastructure, Ansible is for configuring it. They complement each other. I use Terraform to create the VM and Ansible to configure what runs on it."

---

## Week 1: Terraform Core

### Day 1: What is IaC + State Management (TOPIC 01)
- Why IaC (repeat in every interview — its expected)
- What is Terraform state (`terraform.tfstate`)
- State file = source of truth (Terraform compares real infra vs state to decide changes)
- Where state lives: local vs remote (Azure Storage backend)
- **Interview question:** "What happens if someone deletes terraform.tfstate?"
  - Answer: Terraform loses track of real resources. Every resource would be recreated. Never delete state manually.

### Day 2: HCL Syntax + Resources + Variables (TOPIC 02)
- HCL blocks: `resource`, `data`, `variable`, `output`, `provider`, `terraform`
- Resource syntax: `resource "azurerm_resource_group" "example" {}`
- Variables: `variable "name" { type = string }`, `var.name`
- Outputs: `output "rg_id" { value = azurerm_resource_group.example.id }`
- Data sources: `data "azurerm_resource_group" "existing" {}`
- **Key insight:** Data sources READ existing infra, resources CREATE/MANAGE it

### Day 3: Modules (TOPIC 03)
- Why modules: DRY, reusable, versioned, testable
- Module structure: root `main.tf`, `variables.tf`, `outputs.tf`
- Terraform Registry (public modules)
- **Interview question:** "Design a module structure for a 3-tier application"
  - Modules: network/, compute/, database/, each with variables for environment, region, size

### Day 4: Terraform Backend + Workspaces (TOPIC 04)
- Backend = where state is stored
  - Local backend (default) — state on disk, bad for teams
  - AzureRM backend — state in Azure Storage blob, locking via Lease
- Partial configuration (backend config during init)
- Workspaces = separate state files for same config (dev, staging, prod)
- **Interview trap:** "Can you use variables in backend configuration?"
  - Answer: NO. Backend config is loaded before variables. Use partial config with `-backend-config` during init instead.

### Day 5: terraform init / plan / apply / destroy flow (TOPIC 05)
- `terraform init` — downloads providers + modules, configures backend
- `terraform plan` — compares state vs real infra, shows what will change
- `terraform apply` — executes the plan, updates state
- `terraform destroy` — tears down everything in state
- `terraform fmt` / `terraform validate` — code quality
- `terraform state list` / `terraform state show` / `terraform state rm`
- **Interview question:** "What happens between plan and apply?"
  - Plan is saved (or reapplied). Apply reads the plan and executes changes in dependency order (DAG). State is refreshed after each resource.

### Day 6: Lifecycle Rules + Provisioners (TOPIC 06)
- `lifecycle { create_before_destroy = true }` — zero-downtime deployment
- `lifecycle { prevent_destroy = true }` — safety net for critical resources
- `lifecycle { ignore_changes = [tags] }` — ignore metadata changes
- Provisioners: `file`, `remote-exec`, `local-exec`
- **WARNING:** Provisioners are last resort. Use config management (Ansible) instead.

### Day 7: Practice — Deploy a VM on Azure with Terraform
- Resource group -> VNet -> subnet -> public IP -> NIC -> VM
- Use variables for size, location, admin credentials
- Output the public IP
- Run `terraform plan`, `apply`, verify in Azure portal, `destroy`

---

## Week 2: Terraform + Azure + Advanced

### Day 8: azurerm Provider Deep Dive (TOPIC 07)
- Provider config: `features {}` block, subscription_id, tenant_id
- Common resources: `azurerm_resource_group`, `virtual_network`, `subnet`, `public_ip`, `network_interface`, `linux_virtual_machine`
- Data sources for existing resources
- **Key pattern:** Always tag resources — product companies care about cost management

### Day 9: Remote State + State Locking (TOPIC 08)
- Azure Storage backend setup:
  ```hcl
  terraform {
    backend "azurerm" {
      storage_account_name = "tfstate1234"
      container_name       = "tfstate"
      key                  = "prod.terraform.tfstate"
    }
  }
  ```
- State locking prevents concurrent modifications (Azure Storage Lease)
- `terraform force-unlock <lock_id>` — emergency unlock (use carefully)
- State migration: `terraform init -migrate-state` (local -> remote)

### Day 10: Import Existing Infrastructure (TOPIC 09)
- `terraform import azurerm_resource_group.example /subscriptions/.../resourceGroups/myRG`
- State must be empty (no existing resource block with that name) or use `-merge` flag
- After import: write matching config, run `plan` to verify no changes
- **Interview scenario:** "We have 50 VMs created manually in Azure. How to manage with Terraform?"
  - Answer: Write config for one VM, import it, verify with plan. Write module, repeat for remaining VMs. Never import all at once without validation.

### Day 11: Terraform Workspaces + Environment Strategy (TOPIC 10)
- Workspace commands: `terraform workspace new dev`, `workspace select`, `workspace list`
- Variable files: `terraform.tfvars`, `dev.tfvars`, `prod.tfvars`
- Common pattern: `terraform workspace select dev && terraform apply -var-file=dev.tfvars`
- OR use Terragrunt (dont mention unless interviewer brings it up — rarely asked)
- **For interview:** Know workspaces + tfvars files. That covers 90% of environment questions.

### Day 12: Terraform + Azure DevOps Integration (TOPIC 11)
- Pipeline structure for Terraform:
  1. `terraform init` (with remote backend)
  2. `terraform validate` (syntax check)
  3. `terraform plan -out=tfplan` (save plan)
  4. Manual approval gate (for prod)
  5. `terraform apply tfplan`
- Service connection in Azure DevOps to Azure
- Store Terraform variable values as pipeline variables or Variable Groups
- **Key pattern:** Never run `apply` without a saved `plan` in CI/CD

### Day 13: Error Handling + Debugging (TOPIC 12)
- `TF_LOG=DEBUG terraform apply` — verbose logging
- `TF_LOG_PATH=./tf.log` — save logs to file
- Common errors and fixes:
  - `Error acquiring state lock` — force-unlock
  - `Resource already exists` — import it
  - `Provider not found` — re-run init
  - `Invalid index` — check list/map access syntax

### Day 14: Practice — Full Azure Infra with Terraform
Deploy:
- Resource group -> VNet (10.0.0.0/16) -> 2 subnets (public 10.0.1.0/24, private 10.0.2.0/24)
- NSG with SSH allowed (from specific IPs only)
- VM in public subnet with public IP
- ACR (Azure Container Registry) in private subnet
- Remote state in Azure Storage
- Variables for dev/prod with tfvars files

---

## Interview Depth Guide

| Topic | Must Know | Nice to Know | Dont Bother |
|-------|-----------|-------------|-------------|
| State | What it is, remote backend, locking | state migration, `terraform state mv` | State file internals (JSON format) |
| HCL | resource, variable, output, data, provider | for_each, count, dynamic blocks | custom providers |
| Modules | How to create, use registry, pass variables | module versioning, registry publishing | Terragrunt |
| Backend | azurerm backend setup | Partial config, multi-backend | Consul/etcd backends |
| Workspaces | create/select, tfvars per env | workspace CLI in pipelines | Sentinel policies |
| Import | Import single resource, check plan | Import with for_each, terraform state rm | Terraformer tool |
| Provisioners | What they are, why NOT to use them | file/remote-exec/local-exec differences | Any deep provisioner usage |
| Functions | concat, length, lookup, merge, file, templatefile | format, regex, try, can | HashiCorp-defined functions |

## Final Check: Can You Answer These?

1. What happens when you run `terraform plan`?
2. Difference between `terraform apply` and `terraform apply -auto-approve`?
3. How do you handle secrets in Terraform? (Answer: Azure Key Vault data source, NOT in plain text)
4. What is the DAG? How does it help?
5. Why is remote state important for teams?
6. You have 100 resources managed by Terraform. One was deleted manually from Azure Portal. What happens on next `apply`?
7. How do you structure Terraform code for dev/staging/prod?
8. When would you use `count` vs `for_each`?
9. What is `terraform refresh`? (Deprecated — plan now does this)
10. How do you handle large state files? (Answer: Split into smaller configurations or use state environments)

---

*Next: Move to topics/01-state-management.md for Day 1 content*
