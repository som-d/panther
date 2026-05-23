# Linux + Scripting Study Plan

**Target Level:** Mid-level DevOps (3+ YOE) | 7-14 LPA interviews
**Scope:** What's actually asked — NOT everything about Linux
**Rule:** At this level, interviewers test practical debugging and automation, not kernel knowledge.

---

## What Interviewers Actually Test

Linux questions in DevOps interviews at 7-14 LPA level are about:
1. **File operations** — find, grep, awk, sed
2. **Process management** — ps, top, kill
3. **Disk/performance** — df, du, free, iostat
4. **Networking** — curl, netstat, ss, telnet
5. **Scripting** — bash loops, conditionals, functions
6. **Log analysis** — tail, journalctl, less

**They do NOT test:**
- Kernel parameters
- Systemd unit file creation
- SELinux/AppArmor
- Kernel compilation
- NFS/CIFS configuration

---

## 3-Day Crash Course

### Day 1: Essential Commands

**File Operations:**
```bash
# Find files
find /var/log -name "*.log" -mtime -7  # Files modified in last 7 days
find / -type f -size +100M             # Files larger than 100MB
grep -r "ERROR" /var/log/app/         # Search recursively for ERROR
grep -i "timeout" app.log             # Case-insensitive search
awk '{print $1, $4}' access.log       # Extract specific columns
sed 's/oldhost/newhost/g' config.cfg  # Find and replace
```

**Process Management:**
```bash
ps aux | grep nginx      # Find nginx processes
top -o %MEM              # Sort processes by memory usage
kill -9 <PID>            # Force kill (SIGKILL)
kill -15 <PID>           # Graceful shutdown (SIGTERM)
htop                     # Interactive process viewer (if available)
```

**Disk/Performance:**
```bash
df -h                    # Disk usage (human readable)
du -sh /var/log          # Directory size
free -h                  # Memory usage
iostat -x 1             # Disk I/O stats (every second)
vmstat 1                 # Virtual memory stats
```

**Networking:**
```bash
curl -I https://api.example.com   # HTTP headers only
curl -v https://api.example.com   # Verbose (full request/response)
ss -tln                          # Listening TCP ports
ss -tun                          # All TCP/UDP connections
telnet db.example.com 5432       # Test TCP connectivity
nslookup example.com             # DNS lookup
```

**Log Analysis:**
```bash
tail -f /var/log/app.log        # Follow live log
tail -100 /var/log/syslog       # Last 100 lines
journalctl -u nginx --since "1 hour ago"  # Systemd logs
less /var/log/kern.log          # Scrollable file viewer
```

---

### Day 2: Bash Scripting

**Must-know patterns:**

```bash
#!/bin/bash
set -euo pipefail    # Exit on error, undefined var, pipe fail

# Variables
APP_NAME="${1:-default}"  # Default value if no argument
ENV="${ENVIRONMENT:-dev}" # Default from env var or literal

# Conditionals
if [ -f "/etc/nginx/nginx.conf" ]; then
    echo "Config exists"
elif [ "$ENV" = "prod" ]; then
    echo "Production mode"
else
    echo "Unknown"
fi

# Loops
for file in /var/log/app/*.log; do
    echo "Processing $file"
    gzip "$file"
done

# Functions
log() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" >> /var/log/deploy.log
}

# Error handling
if ! curl -sS https://api.example.com/health > /dev/null; then
    echo "Health check failed"
    exit 1
fi

log "Deployment completed"
```

**Common scripting patterns:**
- Check if command exists: `command -v terraform >/dev/null 2>&1`
- Retry logic: `for i in {1..5}; do curl ... && break || sleep 5; done`
- Parse JSON: `echo "$json" | jq '.status'` (jq is not installed by default, but common on DevOps VMs)

---

### Day 3: Common DevOps Scenarios in Scripts

**Scenario 1: Clean old log files**
```bash
#!/bin/bash
LOG_DIR="/var/log/myapp"
RETENTION_DAYS=30

find "$LOG_DIR" -name "*.log" -mtime +$RETENTION_DAYS -exec rm {} \;
echo "Cleaned logs older than $RETENTION_DAYS days from $LOG_DIR"
```

**Scenario 2: Check service health**
```bash
#!/bin/bash
services=("nginx" "postgresql" "docker")

for service in "${services[@]}"; do
    if systemctl is-active --quiet "$service"; then
        echo "OK: $service is running"
    else
        echo "FAIL: $service is not running"
        systemctl restart "$service"
        echo "Restarted $service"
    fi
done
```

**Scenario 3: Backup with timestamp**
```bash
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/app_backup.tar.gz" /var/www/app
echo "Backup created: $BACKUP_DIR/app_backup.tar.gz"
```

---

## Interview Questions

1. **"How do you find the top 5 processes by memory usage?"**
   ```bash
   ps aux --sort=-%mem | head -6
   ```

2. **"How do you check disk space and identify large directories?"**
   ```bash
   df -h
   du -sh /* 2>/dev/null  # Root dirs sorted by size
   du -sh /var/log/
   ```

3. **"How do you debug why a service is not starting?"**
   ```bash
   journalctl -u <service-name> --since "10 minutes ago" -n 50
   systemctl status <service-name>
   /var/log/<service>/error.log
   ```

4. **"Write a script to check if a port is open and send alert if not"**
   ```bash
   #!/bin/bash
   if ! nc -zv localhost 5432 2>/dev/null; then
       echo "Port 5432 is not open" | mail -s "Alert" devops@company.com
   fi
   ```

5. **"How do you search for a string across multiple log files?"**
   ```bash
   grep -r "ERROR\|FATAL\|Exception" /var/log/myapp/
   ```

6. **"How do you pass variables between shell scripts?"**
   ```bash
   # script1.sh
   export DEPLOY_ENV="production"
   
   # script2.sh
   source script1.sh
   echo $DEPLOY_ENV  # "production"
   ```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Find files | `find /path -name "pattern"` |
| Search content | `grep -r "text" /path` |
| Extract column | `awk '{print $2}'` |
| Find and replace | `sed -i 's/old/new/g' file` |
| Top CPU processes | `ps aux --sort=-%cpu` |
| Disk usage | `df -h` |
| Directory size | `du -sh /dir` |
| Listening ports | `ss -tln` |
| Network test | `curl -v url` or `telnet host port` |
| Live log tail | `tail -f /var/log/app.log` |
| Service status | `systemctl status nginx` |
| Check exit code | `echo $?` |

---

*Goal: Know these 30 commands and 3 script patterns. Thats enough for 7-14 LPA interviews.*
