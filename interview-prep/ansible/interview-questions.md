# Ansible Interview Questions (7-14 LPA)

**Note:** You already USE Ansible daily. These questions test if you can EXPLAIN it well.

---

### Q1: "What is Ansible and how does it work?"

**Bad answer:** "Its a configuration management tool."
**Good answer:**
> Ansible is an agentless automation tool. It connects to servers via SSH (WinRM for Windows) and executes tasks defined in YAML playbooks. No agents, no master server, just SSH. The control node pushes configuration to managed nodes. Its idempotent — running the same playbook multiple times produces the same result.

**Why this wins:** Agentless + push + idempotent = shows you understand architecture, not just syntax.

---

### Q2: "Ansible vs Terraform — when to use what?"

**Perfect answer:**
> They solve different problems:
> - **Terraform** is for provisioning infrastructure — creating VMs, networks, load balancers. It manages the infrastructure lifecycle.
> - **Ansible** is for configuring infrastructure — installing software, copying configs, starting services on already-running machines.
>
> I use them together: Terraform creates the Azure VMs and networking, outputs the IPs. Ansible picks up those IPs via dynamic inventory and configures each server. They complement each other perfectly.

---

### Q3: "Why is Ansible considered idempotent?"

> Ansible modules are designed to check the current state before making changes. For example, the `service` module checks if nginx is running. If it IS running and you say `state: started`, Ansible does nothing (no change). If nginx is STOPPED, Ansible starts it. Each module handles this check internally. This is why running the same playbook twice is safe.

---

### Q4: "What are Ansible roles? Why use them?"

> Roles are standardized directory structures for organizing playbooks: `tasks/`, `handlers/`, `templates/`, `files/`, `vars/`, `defaults/`, `meta/`. Benefits:
> 1. **Reusability** — same role across projects
> 2. **Shareability** — Ansible Galaxy
> 3. **Testability** — each role is isolated
> 4. **Readability** — clear separation of concerns
> 5. **Best practice** — every production Ansible setup uses roles

---

### Q5: "How does Ansible handle secrets?"

> Ansible Vault encrypts sensitive data at rest. Encrypted files can be safely committed to git. At runtime:
> - Provide vault password via `--ask-vault-pass`
> - Or use `--vault-password-file` with a script that fetches from Azure Key Vault / HashiCorp Vault
>
> I also use Ansible Vault with Azure Key Vault integration — the vault password is stored in Key Vault, and my pipeline fetches it at runtime.

---

### Q6: "Explain Ansible inventory — static vs dynamic"

> **Static inventory:** A file listing servers:
> ```
> [webservers]
> web01 ansible_host=10.0.1.4
> web02 ansible_host=10.0.1.5
> ```
> 
> **Dynamic inventory:** A script that queries cloud APIs to discover servers. In Azure, you use `azure_rm.py`. Benefits:
> - Auto-scaling groups are automatically included
> - No manual inventory updates
> - Tags-based grouping

---

### Q7: "How do you handle failures in Ansible?"

> Several strategies:
> - `ignore_errors: yes` — Continue even if a task fails
> - `failed_when:` — Custom failure conditions
> - `serial: 2` — Rolling updates (if 2 servers fail, remaining stay up)
> - `max_fail_percentage:` — Abort if too many hosts fail
> - `.retry` files — Retry only failed hosts

---

### Q8: "What are Ansible handlers and when to use them?"

> Handlers are tasks that run only when notified by another task. They run ONCE at the end of the play:
> ```yaml
> tasks:
>   - name: Update nginx config
>     template:
>       src: nginx.conf.j2
>       dest: /etc/nginx/nginx.conf
>     notify: restart nginx  # Triggers handler only if config changed
> 
> handlers:
>   - name: restart nginx
>     service:
>       name: nginx
>       state: restarted
> ```
> Use for: restarting services when config changes, reloading daemon after package install.

---

### Q9: "What are Jinja2 templates in Ansible?"

> Jinja2 templates allow dynamic configuration files using variables:
> ```
> server {
>     listen 80;
>     server_name {{ server_name }};
>     root /var/www/{{ app_name }}/public;
> }
> ```
> Use `template` module to copy and process variables. The template file has `.j2` extension.

---

### Q10: "How do you structure Ansible for a team of 10 DevOps engineers?"

> ```yaml
> ansible/
>   ansible.cfg
>   production/              # Prod inventory + vars
>   staging/                  # Staging inventory + vars
>   requirements.yml          # Galaxy role dependencies
>   playbooks/
>     site.yml                # Master playbook
>     deploy.yml
>     security.yml
>   roles/                    # Shared roles
>     nginx/                  # From Galaxy or custom
>     docker/
>     monitoring/
>   vault/                    # Encrypted secrets
>     prod-vault.yml
>   scripts/                  # Custom scripts
>     azure-dynamic-inv.py
> ```
> Key: Group vars per environment, roles for reusability, vault for secrets, git for version control.

---

## Quick Answer Bank

| Question | One-Liner Answer |
|----------|-----------------|
| What is Ansible? | Agentless automation via SSH |
| Push or pull? | Push (control node pushes to servers) |
| Ansible vs Terraform? | Terraform provisions, Ansible configures |
| Idempotent? | Run twice, same result |
| Dynamic inventory? | Script queries cloud API for live servers |
| Roles? | Reusable, standardized directory structure |
| Handlers? | Run on notify, once at play end |
| Jinja2? | Dynamic templates with variables |
| Vault? | Encrypts secrets at rest |
| Galaxy? | Community role marketplace |

---

*Practice answering these OUT LOUD. You know Ansible — the trick is articulating it well.*
