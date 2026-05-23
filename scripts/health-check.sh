#!/bin/bash
# Health check script for Azure VM
echo "=== Server Health Check ==="
echo "Uptime: $(uptime -p)"
echo "Memory:"
free -h
echo "Disk:"
df -h
echo "=== Done ==="
