import os
import time
import shutil
import smtplib
import importlib.metadata
from datetime import datetime, timezone
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.db import connections
from sqlalchemy import text
from .database import get_db_session

def check_sqlalchemy_db():
    start_time = time.time()
    try:
        session = get_db_session()
        # Execute a simple query to ensure the connection is active
        session.execute(text("SELECT 1")).scalar()
        session.close()
        latency = (time.time() - start_time) * 1000
        
        # Check database type
        from .database import DATABASE_URL
        db_type = "sqlite"
        if DATABASE_URL.startswith("postgresql"):
            db_type = "postgresql"
            
        return {
            "status": "healthy",
            "type": db_type,
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "type": "unknown",
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "error": str(e)
        }

def check_django_db():
    start_time = time.time()
    try:
        conn = connections['default']
        conn.ensure_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        latency = (time.time() - start_time) * 1000
        return {
            "status": "healthy",
            "type": conn.settings_dict.get('ENGINE', '').split('.')[-1],
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "type": "unknown",
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "error": str(e)
        }

def check_stripe():
    stripe_key = os.environ.get('STRIPE_SECRET_KEY')
    if not stripe_key:
        return {
            "status": "unconfigured",
            "message": "STRIPE_SECRET_KEY environment variable is not set."
        }
    
    start_time = time.time()
    try:
        stripe.api_key = stripe_key
        stripe.max_network_retries = 0
        stripe.Balance.retrieve(request_timeout=3.0)
        latency = (time.time() - start_time) * 1000
        return {
            "status": "healthy",
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        return {
            "status": "degraded",
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "error": str(e)
        }

def check_smtp():
    start_time = time.time()
    try:
        host = "smtp.gmail.com"
        port = 587
        s = smtplib.SMTP(host, port, timeout=3.0)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.quit()
        latency = (time.time() - start_time) * 1000
        return {
            "status": "healthy",
            "host": host,
            "port": port,
            "latency_ms": round(latency, 2)
        }
    except Exception as e:
        return {
            "status": "degraded",
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "error": str(e)
        }

def get_system_metrics():
    # Disk Usage
    try:
        disk = shutil.disk_usage(os.path.dirname(os.path.abspath(__file__)))
        total_gb = round(disk.total / (1024**3), 2)
        used_gb = round(disk.used / (1024**3), 2)
        free_gb = round(disk.free / (1024**3), 2)
        percent_used = round((disk.used / disk.total) * 100, 2)
        disk_info = {
            "total_gb": total_gb,
            "used_gb": used_gb,
            "free_gb": free_gb,
            "percent_used": percent_used
        }
    except Exception as e:
        disk_info = {"error": str(e)}

    # Memory Usage (Linux /proc/meminfo)
    mem_info = None
    if os.path.exists('/proc/meminfo'):
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            info = {}
            for line in lines:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].split()[0].strip()
                    info[key] = int(val) * 1024  # KB to Bytes
            
            total = info.get('MemTotal', 0)
            free = info.get('MemFree', 0)
            available = info.get('MemAvailable', free)
            used = total - available
            percent = round((used / total) * 100, 2) if total > 0 else 0
            
            mem_info = {
                "total_mb": round(total / (1024**2), 2),
                "used_mb": round(used / (1024**2), 2),
                "available_mb": round(available / (1024**2), 2),
                "percent_used": percent
            }
        except Exception as e:
            mem_info = {"error": str(e)}

    # Load average
    try:
        load_avg = os.getloadavg()
    except Exception:
        load_avg = None

    return {
        "disk_usage": disk_info,
        "memory_usage": mem_info,
        "load_average": load_avg
    }

def get_dependencies_status():
    packages = [
        'django',
        'sqlalchemy',
        'stripe',
        'psycopg2-binary',
        'whitenoise',
        'python-dotenv'
    ]
    status = {}
    for pkg in packages:
        try:
            version = importlib.metadata.version(pkg)
            status[pkg] = {
                "installed": True,
                "version": version
            }
        except importlib.metadata.PackageNotFoundError:
            try:
                __import__(pkg.replace('-', '_'))
                status[pkg] = {
                    "installed": True,
                    "version": "unknown"
                }
            except ImportError:
                status[pkg] = {
                    "installed": False,
                    "version": None
                }
    return status

def health_check(request):
    """
    Health check API endpoint.
    Verifies database connectivity (SQLAlchemy & Django default), SMTP, Stripe, 
    system resource usage, and application dependencies.
    """
    sqlalchemy_db = check_sqlalchemy_db()
    django_db = check_django_db()
    stripe_status = check_stripe()
    smtp_status = check_smtp()
    system_metrics = get_system_metrics()
    dependencies = get_dependencies_status()
    
    # Determine overall status
    critical_ok = (sqlalchemy_db.get("status") == "healthy") and (django_db.get("status") == "healthy")
    
    if not critical_ok:
        status = "unhealthy"
    elif stripe_status.get("status") == "degraded" or smtp_status.get("status") == "degraded":
        status = "degraded"
    else:
        status = "healthy"
        
    response_data = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "environment": "development" if settings.DEBUG else "production",
        "components": {
            "database_sqlalchemy": sqlalchemy_db,
            "database_django": django_db,
            "stripe_payment": stripe_status,
            "smtp_email": smtp_status
        },
        "system_metrics": system_metrics,
        "dependencies": dependencies
    }
    
    # Return appropriate HTTP status code
    http_status = 200
    if status == "unhealthy":
        http_status = 503
        
    return JsonResponse(response_data, status=http_status)
