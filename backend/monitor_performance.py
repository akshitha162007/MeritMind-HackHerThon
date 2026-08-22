#!/usr/bin/env python3
"""Performance monitoring script for Merit Mind backend."""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

def monitor_api_performance(duration=60, interval=5):
    """Monitor API performance over time."""
    print("\n" + "=" * 70)
    print("MONITORING API PERFORMANCE")
    print("=" * 70)
    print(f"Duration: {duration}s, Interval: {interval}s\n")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        import psutil
        
        client = TestClient(app)
        metrics = defaultdict(list)
        
        start_time = time.time()
        iteration = 0
        
        while time.time() - start_time < duration:
            iteration += 1
            print(f"[Iteration {iteration}] ", end="", flush=True)
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            metrics["cpu"].append(cpu_percent)
            metrics["memory_percent"].append(memory.percent)
            metrics["memory_available"].append(memory.available)
            
            # Test health endpoint
            start = time.time()
            try:
                response = client.get("/api/health")
                elapsed = (time.time() - start) * 1000  # Convert to ms
                metrics["health_endpoint"].append(elapsed)
                print(f"Health: {elapsed:.1f}ms ", end="", flush=True)
            except Exception as e:
                print(f"Health: ERROR ", end="", flush=True)
                metrics["health_endpoint"].append(None)
            
            # Test register endpoint (validation only)
            start = time.time()
            try:
                response = client.post("/api/auth/register", json={})
                elapsed = (time.time() - start) * 1000
                metrics["register_endpoint"].append(elapsed)
                print(f"Register: {elapsed:.1f}ms ", end="", flush=True)
            except Exception as e:
                print(f"Register: ERROR ", end="", flush=True)
                metrics["register_endpoint"].append(None)
            
            # Test login endpoint (validation only)
            start = time.time()
            try:
                response = client.post("/api/auth/login", json={})
                elapsed = (time.time() - start) * 1000
                metrics["login_endpoint"].append(elapsed)
                print(f"Login: {elapsed:.1f}ms", end="", flush=True)
            except Exception as e:
                print(f"Login: ERROR", end="", flush=True)
                metrics["login_endpoint"].append(None)
            
            print()
            
            # Wait for next interval
            elapsed = time.time() - start_time
            if elapsed < duration:
                time.sleep(max(0, interval - (time.time() - start_time + start_time)))
        
        return metrics
    
    except Exception as e:
        print(f"✗ Error during monitoring: {e}")
        return {}

def analyze_metrics(metrics):
    """Analyze collected metrics."""
    print("\n" + "=" * 70)
    print("PERFORMANCE ANALYSIS")
    print("=" * 70 + "\n")
    
    def get_stats(data):
        """Calculate statistics for a data list."""
        valid_data = [x for x in data if x is not None]
        if not valid_data:
            return None
        
        return {
            "min": min(valid_data),
            "max": max(valid_data),
            "avg": sum(valid_data) / len(valid_data),
            "count": len(valid_data),
            "errors": len(data) - len(valid_data)
        }
    
    # Analyze each metric
    for metric_name, data in metrics.items():
        stats = get_stats(data)
        
        if stats is None:
            print(f"{metric_name}: No data")
            continue
        
        if "endpoint" in metric_name:
            print(f"{metric_name}:")
            print(f"  Min: {stats['min']:.1f}ms")
            print(f"  Max: {stats['max']:.1f}ms")
            print(f"  Avg: {stats['avg']:.1f}ms")
            print(f"  Samples: {stats['count']}")
            if stats['errors'] > 0:
                print(f"  Errors: {stats['errors']}")
        else:
            print(f"{metric_name}:")
            print(f"  Min: {stats['min']:.1f}")
            print(f"  Max: {stats['max']:.1f}")
            print(f"  Avg: {stats['avg']:.1f}")
        
        print()

def monitor_system_resources(duration=30, interval=2):
    """Monitor system resources."""
    print("\n" + "=" * 70)
    print("MONITORING SYSTEM RESOURCES")
    print("=" * 70)
    print(f"Duration: {duration}s, Interval: {interval}s\n")
    
    try:
        import psutil
        
        metrics = {
            "cpu": [],
            "memory_percent": [],
            "memory_used": [],
            "disk_percent": []
        }
        
        start_time = time.time()
        iteration = 0
        
        while time.time() - start_time < duration:
            iteration += 1
            
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics["cpu"].append(cpu)
            metrics["memory_percent"].append(memory.percent)
            metrics["memory_used"].append(memory.used)
            metrics["disk_percent"].append(disk.percent)
            
            print(f"[{iteration}] CPU: {cpu:5.1f}% | Memory: {memory.percent:5.1f}% | Disk: {disk.percent:5.1f}%")
            
            elapsed = time.time() - start_time
            if elapsed < duration:
                time.sleep(max(0, interval - (time.time() - start_time + start_time)))
        
        return metrics
    
    except Exception as e:
        print(f"✗ Error during monitoring: {e}")
        return {}

def generate_performance_report(api_metrics, system_metrics):
    """Generate performance report."""
    print("\n" + "=" * 70)
    print("PERFORMANCE REPORT")
    print("=" * 70 + "\n")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "api_metrics": {},
        "system_metrics": {}
    }
    
    # Analyze API metrics
    def get_stats(data):
        valid_data = [x for x in data if x is not None]
        if not valid_data:
            return None
        return {
            "min": min(valid_data),
            "max": max(valid_data),
            "avg": sum(valid_data) / len(valid_data),
            "count": len(valid_data)
        }
    
    for metric_name, data in api_metrics.items():
        stats = get_stats(data)
        if stats:
            report["api_metrics"][metric_name] = stats
    
    for metric_name, data in system_metrics.items():
        stats = get_stats(data)
        if stats:
            report["system_metrics"][metric_name] = stats
    
    # Save report
    report_file = Path(__file__).parent / "performance_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {report_file}")
    
    # Print summary
    print("\nSummary:")
    print("✓ Performance monitoring completed")
    print(f"✓ Report saved to: {report_file}")

def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("MERIT MIND PERFORMANCE MONITOR".center(70))
    print("=" * 70)
    
    # Monitor API performance
    api_metrics = monitor_api_performance(duration=30, interval=2)
    
    # Monitor system resources
    system_metrics = monitor_system_resources(duration=30, interval=2)
    
    # Analyze metrics
    if api_metrics:
        analyze_metrics(api_metrics)
    
    # Generate report
    if api_metrics or system_metrics:
        generate_performance_report(api_metrics, system_metrics)
    
    print("\n" + "=" * 70)
    print("Monitoring completed!")
    print("=" * 70 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
