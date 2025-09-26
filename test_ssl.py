#!/usr/bin/env python3
"""
SSL connection test script for production server diagnosis.
This script tests the same SSL configuration used in anthem.py
to help diagnose certificate issues on the production server.
"""

import asyncio
import aiohttp
import ssl
import sys
import os

async def test_ssl_connection():
    """Test SSL connection to anthem.com using the same logic as anthem.py"""
    url = "https://mproducer.anthem.com"
    
    print("=== SSL Certificate Diagnosis ===")
    print(f"Testing connection to: {url}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Create SSL context with proper configuration (same as in anthem.py)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    
    # Try multiple certificate loading strategies (same as anthem.py)
    cert_loaded = False
    
    # Strategy 1: Load default certificates
    try:
        ssl_context.load_default_certs()
        cert_loaded = True
        print("✓ Successfully loaded default certificates")
    except Exception as e:
        print(f"⚠ Could not load default certificates: {e}")
    
    # Strategy 2: Try common certificate locations (production servers)
    if not cert_loaded:
        cert_paths = [
            '/etc/ssl/certs/ca-certificates.crt',  # Ubuntu/Debian
            '/etc/ssl/certs/ca-bundle.crt',        # CentOS/RHEL
            '/etc/pki/tls/certs/ca-bundle.crt',    # CentOS/RHEL alternative
            '/usr/local/share/ca-certificates/ca-certificates.crt',  # Alternative
            '/etc/ssl/cert.pem',                   # macOS/FreeBSD
            '/usr/local/etc/ssl/cert.pem',         # macOS Homebrew
        ]
        
        for cert_path in cert_paths:
            try:
                if os.path.exists(cert_path):
                    ssl_context.load_verify_locations(cert_path)
                    cert_loaded = True
                    print(f"✓ Successfully loaded certificates from {cert_path}")
                    break
                else:
                    print(f"⚠ Certificate file not found: {cert_path}")
            except Exception as e:
                print(f"⚠ Could not load certificates from {cert_path}: {e}")
                continue
    
    if not cert_loaded:
        print("⚠ No SSL certificates found. This will likely cause connection issues.")
        print("⚠ Consider updating certificate authorities on the production server.")
    
    print()
    print("=== Testing SSL Connection ===")
    
    # Create connector with SSL context
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            print(f"Attempting SSL connection to {url}...")
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                print(f"✓ SSL connection successful! Status: {resp.status}")
                print(f"✓ Content-Type: {resp.headers.get('content-type', 'N/A')}")
                print(f"✓ Server: {resp.headers.get('server', 'N/A')}")
                return True
    except aiohttp.ClientConnectorCertificateError as e:
        print(f"✗ SSL Certificate Error: {e}")
        print("This is the same error you're seeing in the application.")
        print("The SSL certificate verification is failing.")
        return False
    except aiohttp.ClientConnectorError as e:
        print(f"✗ Connection Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

async def main():
    """Main test function"""
    print("SSL Connection Test for Anthem API - Production Server Diagnosis")
    print("=" * 70)
    
    success = await test_ssl_connection()
    
    print()
    print("=== Results ===")
    if success:
        print("✓ SSL configuration is working correctly!")
        print("✓ The anthem.py SSL fix should resolve the certificate verification errors.")
        print("✓ Your application should now work without SSL errors.")
    else:
        print("✗ SSL connection failed.")
        print("✗ This confirms the SSL certificate issue on the production server.")
        print()
        print("=== Recommended Actions ===")
        print("1. Update system certificates:")
        print("   sudo apt-get update && sudo apt-get install ca-certificates")
        print("   sudo update-ca-certificates")
        print()
        print("2. Or try manual certificate installation:")
        print("   wget https://curl.se/ca/cacert.pem -O /etc/ssl/certs/ca-certificates.crt")
        print("   sudo update-ca-certificates")
        print()
        print("3. After updating certificates, run this test again to verify the fix.")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
