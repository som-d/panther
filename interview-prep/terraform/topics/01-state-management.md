# Topic 01: Terraform State Management

**Why This Is The Most Important Topic**

In every Terraform interview, state is THE defining topic. If you understand state deeply, you understand Terraform. If you don't, you look like a beginner who just runs commands without understanding what happens.

---

## 1. What Is Terraform State?

Terraform state (`terraform.tfstate`) is a JSON file that maps your configuration to real-world infrastructure.

```json
{
  "version": 4,
  "terraform_version": "1.9.0",
  "resources": [
    {
      "module": "root",
      "mode": "managed",
      "type": "azurerm_resource_group",
      "name": "main",
      "provider": "provider[\"registry.terraform.io/hashicorp/azurerm\"]",
      "instances": [
        {
          "schema_version": 0,
          "attributes": {
            "id": "/subscriptions/.../resourceGroups/my-app-rg",
            "name": "my-app-rg",
            "location": "eastus",
            "tags": {}
          }
        }
      ]
    }
  ]
}
```

**Key information stored:**
- Resource metadata (ID, type, provider)
- Resource attributes (names, IPs, endpoints — everything Terraform knows)
- Dependencies (implicit from references)
- Metadata (Terraform version, serial number for locking)

---

## 2. What Does State DO?

### a) Mapping (Configuration -> Real World)
When you write:
```hcl
resource "azurerm_resource_group" "main" {
  name     = "my-app-rg"
  location = "eastus"
}
```

State records that this block maps to the Azure resource `/subscriptions/.../resourceGroups/my-app-rg`. On the next `plan`, Terraform reads state and checks Azure to see if anything changed.

### b) Performance
Without state, Terraform would need to query every single Azure resource on every `plan`. With state, it only checks what's in state (much faster).

### c) Dependency Graph
State records which resources depend on which. When you reference one resource in another:
```hcl
resource "azurerm_network_interface" "main" {
  # Depends on resource group (implicit dependency)
  resource_group_name = azurerm_resource_group.main.name
}
```
Terraform builds a Directed Acyclic Graph (DAG) and creates resources in order: RG -> NIC -> VM.

### d) Diff Calculation
`terraform plan` = Desired (config) vs Actual (state + Azure API)

If config says "2 VMs" and state says "2 VMs" and Azure has "2 VMs" — nothing to do.
If config says "3 VMs" but state says "2 VMs" — Terraform will create 1 more.
If Azure has the VM but state doesn't — Terraform sees a change it doesn't know about.

---

## 3. What Happens During terraform plan?

Step by step:

1. **Load configuration** — read all .tf files
2. **Refresh state** — query Azure API for each resource in state, update state with current values
3. **Compare** — config vs refreshed state
4. **Generate diff** — what to create, modify, or delete
5. **Output** — display the plan (or save with `-out=tfplan`)

**Key insight:** Terraform does NOT compare config vs Azure directly. It compares config vs state, and state vs Azure (refresh). This is why having correct state is critical.

---

## 4. State File Location

### Local State (default)
- File: `terraform.tfstate` in your working directory
- Backup: `terraform.tfstate.backup` (previous version)
- **Problem for teams:** Stored locally. If 2 people run apply, they overwrite each others state.
- **Never commit to git:** `*.tfstate*` in .gitignore

### Remote State (Azure Storage — production)
```hcl
terraform {
  backend "azurerm" {
    storage_account_name = "mytfstate"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
  }
}
```
- State stored in Azure Blob Storage
- Locking via Azure Storage Lease (prevents concurrent writes)
- Shared across the team
- Encrypted at rest (Azure Storage encryption)
- Access controlled via Azure RBAC

---

## 5. State Locking

When you run `terraform apply`, Terraform acquires a lock on the state file.

- **Local:** Lock file (`.terraform.tfstate.lock.info`) — only prevents concurrent applies from same directory
- **Remote (Azure Storage):** Lease on the blob — prevents ANY concurrent apply from ANY machine

**What happens if lock fails?**
```
Error: Error acquiring the state lock

Error message: lock was already acquired
Lock Info:
  ID:        <lock-id>
  Path:      tfstate/production.terraform.tfstate
  Operation: OperationTypeApply
  Who:       user@company.com
  Version:   1.9.0
  Created:   2026-05-21 10:30:00
```

**Force unlock (emergency only):**
```bash
terraform force-unlock <lock-id>
```
Only use when:
1. The process that held the lock crashed
2. You're SURE no other Terraform operation is running
3. You've verified in Azure Storage that the lease is stale

---

## 6. State Manipulation Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `terraform state list` | List all resources | `terraform state list` -> `azurerm_resource_group.main` |
| `terraform state show` | Show resource details | `terraform state show azurerm_resource_group.main` |
| `terraform state rm` | Remove from state (NOT destroy) | `terraform state rm azurerm_vm.main` (stops managing it) |
| `terraform state mv` | Rename/move resource in state | `terraform state mv azurerm_vm.old azurerm_vm.new` |
| `terraform state pull` | Download current state | `terraform state pull > tfstate.json` |
| `terraform state push` | Upload state (dangerous) | Only use when you know what you're doing |

---

## 7. State File Sensitivity (CRITICAL)

State file contains **ALL resource attributes** including secrets:
```json
"admin_password": "SuperSecret123!"
```

**Never:**
- Commit state to git ❌
- Share state file via email ❌
- Store state in unencrypted location ❌

**Protect state with:**
1. Remote backend with encryption (Azure Storage)
2. RBAC — only DevOps team can access state storage
3. Use Key Vault for secrets (they still appear in state, but KV reference is better than plain text)
4. State file audit logs in Azure

---

## 8. Common State Problems & Solutions

### Problem 1: State file corrupted
**Symptom:** `terraform plan` fails with JSON parse error
**Solution:** Restore from `terraform.tfstate.backup` (previous version) or from Azure Storage blob versioning

### Problem 2: Resource deleted outside Terraform
**Symptom:** Plan shows resource will be created (but it already exists)
**Solution:** `terraform state rm <resource>` or import it

### Problem 3: State file too large
**Symptom:** Slow operations, memory issues
**Solution:** Split into multiple Terraform configurations (separate state files per component)

### Problem 4: Stale lock
**Symptom:** "Error acquiring the state lock"
**Solution:** Verify no other process running, then `terraform force-unlock`

### Problem 5: Wrong workspace
**Symptom:** Changes applied to wrong environment
**Solution:** Use separate state storage containers per environment, never share

---

## 9. Interview-Style Questions on State

**Q: "What happens if two people run terraform apply simultaneously?"**
A: With remote state + locking, one acquires the lock and executes. The other waits or fails (depending on timeout). With local state, both run, the last one wins, and state is inconsistent.

**Q: "Can I recover state if I lose the state file?"**
A: Partially. Run `terraform import <resource> <id>` for each resource. Or use tools like Terraformer to generate state. But this is painful — which is why remote state backup is essential.

**Q: "Should state be committed to git?"**
A: NEVER. State contains secrets and is not human-readable. Use remote backend for sharing state across the team.

**Q: "What is the difference between terraform state rm and terraform destroy?"**
A: `state rm` removes the resource from state (Terraform forgets it — resource still exists in Azure). `destroy` deletes the actual infrastructure AND removes from state.

---

## 10. Hands-On Exercise

```bash
# Initialize with local state
mkdir tf-state-lab && cd tf-state-lab
echo '
resource "azurerm_resource_group" "test" {
  name     = "tf-state-lab-rg"
  location = "eastus"
}
' > main.tf

terraform init
terraform apply -auto-approve

# Look at state file
cat terraform.tfstate | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Remove from state (resource still exists in Azure!)
terraform state rm azurerm_resource_group.test

# Plan shows it will be recreated
terraform plan

# Import it back
terraform import azurerm_resource_group.test /subscriptions/.../resourceGroups/tf-state-lab-rg

# Now destroy
terraform destroy -auto-approve
```

---

## Summary: The State Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────┐
│                    Terraform State                              │
├─────────────────────────────────────────────────────────────────┤
│  What it is:  JSON mapping of config -> real infrastructure     │
│  Where:       Local (terraform.tfstate) or Remote (Azure)       │
│  Purpose:     Track, diff, dependency graph, performance        │
│  Sensitive:   YES — contains all resource attributes + secrets  │
│  Locking:     Yes (local file or Azure Storage Lease)           │
│  Team use:    ALWAYS use remote backend                         │
│  Git:         NEVER commit                                      │
└─────────────────────────────────────────────────────────────────┘
```

**You have mastered state when you can:**
- Explain why state exists (not just what it is)
- Set up remote backend in Azure Storage
- Handle lock errors
- Recover from state corruption
- Explain why state is sensitive and how to protect it

---

*Next: 02-hcl-syntax-resources-variables.md*
