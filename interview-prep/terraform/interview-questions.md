# Terraform Interview Questions (7-14 LPA Level)

**Source:** Aggregated from Indian product company DevOps interviews
**Level:** Mid-level (3-5 YOE)
**Format:** Question -> Expected Answer -> Why It Matters

---

## Fundamentals

### Q1: "What is IaC and why do we need it?"
**Expected Answer:**
> Infrastructure as Code means managing infrastructure (VMs, networks, databases) through machine-readable definition files, not manual processes. Benefits:
> - **Version control:** Infra changes are tracked in git
> - **Repeatability:** Same config = same infra every time
> - **Audit trail:** Who changed what and when
> - **Self-documentation:** Config files document the infra
> - **Disaster recovery:** Recreate entire infra from code

**Why it matters:** Every interviewer starts here. If you cant articulate IaC value, they assume you don't understand the fundamentals.

---

### Q2: "Terraform vs Ansible — why would you use both?"
**Expected Answer:**
> Terraform is a provisioning tool — it creates infrastructure (VMs, networks, load balancers). Ansible is a configuration management tool — it configures software on existing infrastructure (install packages, copy files, start services).
>
> In practice: Use Terraform to create a VM and a load balancer. Use Ansible to install Nginx on the VM and deploy the application. They complement each other.

**Why it matters:** You know Ansible. They WILL ask this to test if you understand the distinction.

---

### Q3: "Explain the Terraform workflow"
**Expected Answer:**
> 1. `terraform init` — Initializes the working directory, downloads providers and modules, configures the backend
> 2. `terraform plan` — Reads current state, compares with real infrastructure, shows proposed changes (no execution)
> 3. `terraform apply` — Executes the changes planned, updates state file
> 4. `terraform destroy` — Tears down all resources tracked in state
>
> Between plan and apply, Terraform builds a dependency graph (DAG) and executes resources in the correct order.

**Why it matters:** Shows you understand the lifecycle, not just commands.

---

### Q4: "What is terraform state? Why is it important?"
**Expected Answer:**
> State is Terraforms mapping between real-world infrastructure and your configuration. It stores resource metadata, dependencies, and attributes.
>
> Importance:
> - **Mapping:** Knows which Azure resource corresponds to which config block
> - **Performance:** Doesnt need to query all resources on every plan
> - **Dependency resolution:** Builds the graph for correct execution order
> - **Diff calculation:** Compares desired (config) vs actual (state) to determine changes

**Why it matters:** State is THE most misunderstood concept. If you nail this, you stand out.

---

### Q5: "State file is sensitive. How do you handle it?"
**Expected Answer:**
> - Never commit state file to git (add `*.tfstate*` to .gitignore)
> - Use remote backend (Azure Storage with encryption at rest)
> - Enable state locking to prevent concurrent modification
> - Restrict access via Azure RBAC — only DevOps team members should access the storage container
> - For secrets in state (like VM passwords), use Azure Key Vault — store secret in KV, reference it in Terraform

**Why it matters:** Shows security awareness — product companies care deeply about this.

---

## Intermediate

### Q6: "Remote backend vs local backend — when to use what?"
**Expected Answer:**
> - **Local backend:** Single developer, learning, POC. State stored on local disk. Simple but no team collaboration.
> - **Remote backend (Azure Storage):** Team environment. State stored in Azure Storage blob. Provides state locking, sharing, and backup. Required for CI/CD pipelines.
>
> Always use remote backend in production — even for single-person projects. Its a habit that prevents future pain.

**Why it matters:** Tests practical experience. Anyone who says "local is fine for production" fails.

---

### Q7: "What happens to state when a resource is deleted manually from Azure Portal?"
**Expected Answer:**
> On the next `terraform plan`, Terraform detects that the resource exists in state but not in reality. It will show:
> ```
>   # azurerm_virtual_network.example has been deleted outside of Terraform
>   resource "azurerm_virtual_network" "example" will be created
> ```
>
> Terraform will recreate the resource on the next `apply`. To fix without recreation:
> 1. Run `terraform state rm azurerm_virtual_network.example` to remove it from state
> 2. OR run `terraform refresh` (deprecated — plan now does this) to update state
> 3. Or import the existing resource

**Why it matters:** Drift detection is a key Terraform feature. Shows you know how to handle real-world scenarios.

---

### Q8: "Explain Terraform modules and why they are useful"
**Expected Answer:**
> Modules are self-contained packages of Terraform configurations. They:
> - **Promote reuse:** Same config for dev/staging/prod with different variable values
> - **Abstract complexity:** Hide implementation details behind variables
> - **Version control:** Modules can be versioned (e.g., `version = "~> 2.0"`)
> - **Standardize:** Enforce company standards (naming, tagging, sizing)
>
> Module structure: `main.tf` (resources), `variables.tf` (inputs), `outputs.tf` (exposed values)

**Why it matters:** Module design is a common interview topic — they want to see you think in abstractions.

---

### Q9: "What is the difference between count and for_each?"
**Expected Answer:**
> - `count`: Creates N copies of a resource, indexed by number (0, 1, 2...). If you insert/remove an element from the middle, Terraform recreates subsequent resources (shifting index).
> - `for_each`: Creates resources from a map or set of strings, keyed by the map key. Adding/removing elements only affects those specific resources — no shifting.
>
> **Use `for_each`** when the set of resources might change over time. Use `count` only for simple, fixed-size scenarios.

**Why it matters:** This is a common gotcha that distinguishes experienced users from beginners.

---

### Q10: "How do you handle Terraform in CI/CD?"
**Expected Answer:**
> ```yaml
> - script: terraform init -backend-config=backend.tfvars
> - script: terraform validate
> - script: terraform plan -out=tfplan
> - script: terraform apply tfplan  # After manual approval for prod
> ```
>
> Key practices:
> - Run `plan` on every PR (as validation)
> - Require manual approval for production `apply`
> - Store backend config and variable values securely (Azure DevOps Variable Groups linked to Key Vault)
> - Use separate service connections per environment (dev, staging, prod)

**Why it matters:** CI/CD integration is what product companies actually need — not just running Terraform locally.

---

## Advanced (for 10-14 LPA roles)

### Q11: "You have 3 environments (dev, staging, prod). How would you structure Terraform?"
**Expected Answer:**
> Option 1 — **Directory structure per environment:**
> ```
> terraform/
>   dev/
>     main.tf
>     dev.tfvars
>   staging/
>     main.tf
>     staging.tfvars
>   prod/
>     main.tf
>     prod.tfvars
>   modules/
>     network/
>     compute/
> ```
>
> Option 2 — **Workspaces:**
> ```
> terraform workspace new dev
> terraform workspace new staging
> terraform workspace new prod
> terraform apply -var-file="${terraform.workspace}.tfvars"
> ```
>
> I prefer Option 1 for production because each environment has its own state file, backend config, and access control. Workspaces are simpler but make it easier to accidentally run changes in the wrong environment.

**Why it matters:** Shows real architecture thinking, not just textbook knowledge.

---

### Q12: "How do you handle secrets in Terraform?"
**Expected Answer:**
> Never hardcode secrets. Options:
> 1. **Azure Key Vault** (recommended):
>    ```hcl
>    data "azurerm_key_vault_secret" "admin_password" {
>      name         = "vm-admin-password"
>      key_vault_id = data.azurerm_key_vault.example.id
>    }
>    ```
> 2. **Environment variables:** `TF_VAR_db_password` pattern
> 3. **Azure DevOps Variable Groups** (linked to Key Vault)
> 4. **Sensitive output:** `output "password" { sensitive = true }`
>
> Even with these, secrets end up in state file. Use Azure Storage encryption at rest + restrict state file access via RBAC.

**Why it matters:** Security is the #1 concern for product companies. Show you take it seriously.

---

### Q13: "Explain Terraform lifecycle rules with examples"
**Expected Answer:**
> ```hcl
> resource "azurerm_virtual_machine" "example" {
>   lifecycle {
>     create_before_destroy = true   # Zero-downtime deployment
>     prevent_destroy       = true   # Critical resource protection
>     ignore_changes        = [      # Ignore specific attribute changes
>       tags,
>       vm_size
>     ]
>   }
> }
> ```
> - `create_before_destroy`: Creates new resource before destroying old one (zero-downtime)
> - `prevent_destroy`: Prevents accidental deletion of critical resources
> - `ignore_changes`: Ignores changes to specified attributes (useful when something else modifies them)

**Why it matters:** Shows you understand production deployment patterns, not just basic creation.

---

### Q14: "What is a data source in Terraform? Give an example"
**Expected Answer:**
> A data source reads information from existing infrastructure that Terraform doesn't manage. It's read-only.
>
> Example: Read an existing Azure Resource Group
> ```hcl
> data "azurerm_resource_group" "existing" {
>   name = "production-rg"
> }
>
> resource "azurerm_virtual_network" "vnet" {
>   name                = "production-vnet"
>   location            = data.azurerm_resource_group.existing.location
>   resource_group_name = data.azurerm_resource_group.existing.name
>   address_space       = ["10.0.0.0/16"]
> }
> ```

**Why it matters:** Data sources vs resources is a common interview point of confusion. Clear answer = clear understanding.

---

### Q15: "What is `terraform import` and when would you use it?"
**Expected Answer:**
> `terraform import` brings existing manually-created infrastructure under Terraform management.
>
> ```bash
> terraform import azurerm_resource_group.main /subscriptions/123/.../resourceGroups/prod-rg
> ```
>
> Workflow:
> 1. Write the resource block in .tf file
> 2. Run `terraform import` with resource address and Azure resource ID
> 3. Run `terraform plan` to verify state matches config (no changes expected)
> 4. If there are differences, adjust config to match real infrastructure
>
> Use when migrating from manual/Azure Portal created infrastructure to Terraform management.

**Why it matters:** Real companies have existing infrastructure. Import is how they adopt Terraform.

---

## Practical Scenario Questions

### Q16: "Your terraform apply fails midway. What do you do?"
**Answer:**
> 1. Check error message — Terraform provides partial state update
> 2. Identify which resources were created before failure
> 3. Fix the issue in config
> 4. Run `terraform plan` again — Terraform will detect already-created resources and proceed
> 5. Run `terraform apply` to continue from where it failed
>
> Key: Terraform updates state incrementally. Resources created before failure are tracked in state and wont be recreated.

---

### Q17: "Someone ran terraform apply and it changed production resource. How do you prevent this?"
**Answer:**
> Multiple layers of protection:
> 1. **CI/CD pipeline:** Plan is reviewed before apply
> 2. **Manual approval gate:** Production requires explicit approval
> 3. **Separate state files:** Each environment has its own state
> 4. **RBAC:** Limit who can access production state storage
> 5. **`prevent_destroy`:** On critical production resources
> 6. **Sentinel policies** (HashiCorp premium) — policy as code

---

### Q18: "How do you test Terraform code?"
**Answer:**
> - `terraform fmt -check` — formatting
> - `terraform validate` — syntax and basic validation
> - `terraform plan` — dry-run to verify changes
> - `checkov` or `tfsec` — security scanning
> - terratest (Go framework) — integration testing (rarely needed at this level)

---

## Common Mistakes Candidates Make

| Mistake | Why It Hurts | Correct Approach |
|---------|-------------|------------------|
| "Terraform is like Ansible" | Shows confusion between provisioning and config management | Explain they complement each other |
| "State file is not important" | Shows lack of production experience | Explain state is central to Terraform |
| Hardcode secrets in .tf files | Security red flag | Use Key Vault or environment variables |
| "I use count for everything" | Shows limited knowledge | Explain for_each vs count tradeoffs |
| Cant explain terraform init vs plan vs apply | Shows no hands-on experience | Walk through the workflow naturally |

---

## Quick Cheat Sheet (Last-Minute Revision)

| Command | What It Does | When To Use |
|---------|-------------|-------------|
| `terraform init` | Download providers, init backend | First time, after adding providers/modules |
| `terraform plan` | Show what will change | Before EVERY apply |
| `terraform apply` | Execute changes | After plan review |
| `terraform destroy` | Delete everything in state | Cleanup, never on prod |
| `terraform fmt` | Format code | Before commit |
| `terraform validate` | Check syntax | Before plan |
| `terraform import` | Add existing infra to state | Migration |
| `terraform state list` | List resources in state | Debugging |
| `terraform force-unlock` | Remove stale lock | Emergency only |

---

*Last updated: 21 May 2026 | Use with study-plan.md + topics/* 
