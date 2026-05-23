# Ansible Interview Study Plan

**Target:** DevOps Engineer, 3+ YOE | 7-14 LPA interviews
**Context:** You already USE Ansible daily at Wipro — this folder is about interview ARTICULATION, not learning from scratch.
**Goal:** Convert your hands-on experience into interview-winning answers.

---

## Why Ansible Matters in Interviews

At Indian product companies, Ansible questions test:
1. **Terraform vs Ansible understanding** — can you explain when to use each?
2. **Real production experience** — have you actually managed servers with it?
3. **Architecture knowledge** — do you understand push vs pull, inventory, modules?

Since you use Ansible at Wipro, you have a HUGE advantage. Dont waste it.

---

## Interview Gap Analysis (What You Know vs What They Ask)

| You Know (Wipro) | Interviewers Want To Hear |
|-----------------|--------------------------|
| Running playbooks | WHY you chose Ansible over alternatives |
| Writing basic tasks | How you STRUCTURE roles for reusability |
| Managing a few servers | How you handle 100+ servers, rolling updates, error handling |
| Using jinja2 templates | When to use template vs copy module |
| Inventory files | Dynamic inventory from cloud (AWS/Azure) |

---

## 1. Core Concepts (Review, Dont Re-learn)

### Ansible Architecture

```
Control Node (your laptop/runner)
    │
    ├── Playbook (YAML)
    ├── Inventory (hosts)
    └── Roles (structured)
            │
            ▼
    Managed Nodes (via SSH, no agent required!)
```

**Key interview points (say these):**
- **Agentless** — uses SSH, no software on managed nodes
- **Push-based** — control node pushes config TO servers (unlike Puppet/Chef which pull)
- **Idempotent** — running same playbook multiple times = same result
- **Declarative** — you describe the desired state, Ansible figures out how

### vs Terraform (CRITICAL interview question)
```diff
+ Say this when asked "Ansible vs Terraform?"

! Terraform PROVISIONS infrastructure (create VMs, networks, load balancers)
! Ansible CONFIGURES infrastructure (install software, copy files, start services)
! They COMPLEMENT each other:
!   Terraform creates the VM
!   Ansible configures what runs ON the VM
```

---

## 2. Key Modules You Must Explain Well

| Module | What It Does | Interview Answer Angle |
|--------|-------------|----------------------|
| `copy` | Copy file from control to managed node | "I use copy for config files, templates for dynamic files" |
| `template` | Copy with Jinja2 variable substitution | "Template processes variables before copying — critical for env-specific configs" |
| `service` | Start/stop/restart services | "I use service with state=restarted when config changes, with handlers" |
| `yum/apt` | Package management | "I use package module (cross-platform) instead of yum/apt" |
| `command/shell` | Run arbitrary commands | "Last resort — only when no module exists. Not idempotent" |
| `uri` | HTTP requests | "For API calls and health checks from playbooks" |
| `debug` | Print variables | "Essential for troubleshooting complex templates" |
| `wait_for` | Wait for port/service | "Polls until a port is open — critical for rolling updates" |

---

## 3. Ansible Architecture Questions

**Q: "How do you structure Ansible for a large environment?"**

Expected answer:
```
ansible/
  ansible.cfg              # Config: forks=50, host_key_checking=False
  production.yml           # Prod inventory (or dynamic inventory script)
  staging.yml              # Staging inventory
  requirements.yml         # Galaxy roles
  site.yml                 # Master playbook
  
  group_vars/
    all.yml                # Variables for ALL hosts
    prod.yml               # Prod-specific variables
    staging.yml            # Staging-specific variables
    
  host_vars/
    web01.yml              # Single host variables
    
  roles/
    nginx/
      tasks/main.yml       # What nginx role does
      handlers/main.yml    # Restart nginx on config change
      templates/nginx.conf.j2  # Config template
      vars/main.yml        # Default variables
      defaults/main.yml    # Overridable defaults
    common/                # Base setup for all servers
    monitoring/            # Monitoring agent setup
```

**Q: "Explain Ansible roles and why use them"**
> Roles organize playbooks into reusable components. A role has a standard directory structure (tasks, handlers, templates, files, vars, defaults, meta). Benefits:
> - Reuse across playbooks
> - Share via Ansible Galaxy
> - Clear separation of concerns
> - Testable independently

**Q: "What is Ansible Galaxy?"**
> Ansible Galaxy is a hub for community-maintained roles. You can download pre-built roles for common tasks (install Nginx, configure Docker, etc.) using `ansible-galaxy install username.rolename`.

---

## 4. Advanced Topics for Senior Roles

### Ansible Vault
```bash
ansible-vault create secrets.yml     # Create encrypted file
ansible-vault view secrets.yml       # View decrypted
ansible-vault edit secrets.yml       # Edit encrypted
ansible-vault encrypt existing.yml   # Encrypt existing
ansible-playbook site.yml --ask-vault-pass  # Run with vault password
```

**Interview answer:**
> "I use Ansible Vault for secrets. Store vault password in Azure Key Vault or HashiCorp Vault. Never commit unencrypted secrets."

### Dynamic Inventory
Instead of static `production.ini`, use a script that queries cloud API:
```bash
# For Azure:
ansible-inventory -i azure_rm.py --list
```

**Why it matters:** Product companies have auto-scaling — servers come and go. Static inventory breaks. Dynamic inventory = servers discovered automatically.

### Rolling Updates
```yaml
- name: Rolling update of web servers
  hosts: webservers
  serial: 2  # Update 2 servers at a time
  tasks:
    - name: Stop nginx
      service:
        name: nginx
        state: stopped
    - name: Deploy new code
      synchronize:
        src: /path/to/new/code/
        dest: /var/www/app/
    - name: Start nginx
      service:
        name: nginx
        state: started
```

**Key insight:** `serial: 2` means update 2 servers, wait, update next 2. Zero downtime.

---

## 5. Production Issues & Tips (CRITICAL — User doesnt see these at Wipro)

### Common Production Issues
| Issue | Symptom | Fix |
|-------|---------|-----|
| SSH timeout on 100+ servers | Playbook hangs | Increase `forks=50` in ansible.cfg |
| Jinja2 template error | "undefined variable" | Check group_vars/host_vars order — more specific wins |
| Idempotency failure | "changed" every run | Module not idempotent (command/shell). Use proper modules |
| SSH host key changed | "Host key verification failed" | Set `host_key_checking = False` (or manage known_hosts) |
| Vault password in git | Secret leaked! | Never commit vault password. Use --vault-password-file or env var |

### Pro Tips
1. **`--check` mode:** Run `ansible-playbook site.yml --check` to see what would change (like terraform plan)
2. **`--diff` mode:** Show what changes in files
3. **`--step` mode:** Interactive confirmation before each task (great for debugging)
4. **`ansible-doc -l | grep azure`:** List all Azure modules
5. **Use `retry` files:** After failed run, Ansible creates `.retry` file with failed hosts. Use `--limit @site.retry` to retry only failed hosts

### Tag Strategy
```yaml
tasks:
  - name: Install nginx
    apt:
      name: nginx
    tags: [packages, nginx]

  - name: Configure nginx
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    tags: [config, nginx]
```
Run only specific parts: `ansible-playbook site.yml --tags "nginx"`

---

## 6. Ansible + Terraform Together (Key Interview Topic)

```
Terraform creates:
  ├── Azure Resource Group
  ├── VNet + Subnet
  ├── VM (with public IP)
  └── Output: VM IPs and SSH keys

Ansible uses those IPs:
  ├── Dynamic inventory from terraform output
  ├── Installs Docker, Nginx, application
  ├── Configures firewall rules
  └── Deploys application code
```

**Interview answer:**
> "In my workflow, Terraform provisions the infrastructure and outputs the IP addresses. Ansible picks up those IPs via dynamic inventory or a generated inventory file, and configures the servers. This is the standard 'Terraform + Ansible' pattern — provision with Terraform, configure with Ansible."

---

## 7. Ansible vs Other Tools (Interview Answers)

| Tool | Comparison Point | Your Answer |
|------|-----------------|-------------|
| **Ansible vs Chef/Puppet** | Agentless vs agent-based | "Ansible is simpler — no agents, no master, just SSH" |
| **Ansible vs SaltStack** | Push vs push+event | "Ansible's push model is simpler for most use cases" |
| **Ansible vs Terraform** | Config vs provision | Already covered above (CRITICAL question) |
| **Ansible vs Shell scripts** | Idempotency | "Ansible modules are idempotent. Shell scripts are not. A shell script that runs twice might break things" |

---

## Quick Interview Cheat Sheet

```
ANSIBLE IN 5 POINTS:
1. Agentless (SSH only) — no software on managed nodes
2. Push-based — control node pushes to servers
3. Idempotent — safe to run repeatedly
4. Declarative YAML — describe desired state
5. Roles for reusability, Vault for secrets

ALWAYS SAY in interviews:
"Ansible and Terraform complement each other.
 Terraform provisions the VM, Ansible configures it."

PRODUCTION TIPS to mention:
- Dynamic inventory for auto-scaling
- serial: 2 for zero-downtime rolling updates
- --check mode for dry runs
- ansible.cfg with forks=50 for speed
```

---

*Next: interview-questions.md for practice*
