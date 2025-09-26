# SSL Certificate Fix for Production Server

## Problem
The application is experiencing SSL certificate verification errors when connecting to `mproducer.anthem.com:443` on the production server:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

## Solution Implemented

### 1. Enhanced SSL Configuration
The `anthem.py` file has been updated with robust SSL certificate handling that:
- Tries multiple certificate loading strategies
- Provides fallback options for different server environments
- Includes comprehensive error handling and logging
- Configures more permissive SSL settings for problematic domains

### 2. Configuration Options
Added SSL configuration options in `config.ini`:

```ini
[SSL]
# SSL verification settings
VERIFY = true
DISABLE_VERIFICATION = false
PERMISSIVE_SSL = true
```

### 3. Production Server Certificate Fixes

#### Option A: Update System Certificates (Recommended)
```bash
# For Ubuntu/Debian servers:
sudo apt-get update
sudo apt-get install ca-certificates
sudo update-ca-certificates

# For CentOS/RHEL servers:
sudo yum update ca-certificates
# or
sudo dnf update ca-certificates
```

#### Option B: Manual Certificate Installation (What Fixed This Issue)
If the above doesn't work, manually install the latest certificates:

```bash
# Download the latest Mozilla CA bundle
wget https://curl.se/ca/cacert.pem -O /tmp/cacert.pem
sudo cp /tmp/cacert.pem /usr/local/share/ca-certificates/mozilla-ca-bundle.crt
sudo update-ca-certificates

# If that doesn't work, try:
sudo cp /tmp/cacert.pem /etc/ssl/certs/ca-certificates.crt
sudo update-ca-certificates
```

**Note**: This approach successfully resolved the SSL certificate issue by including the missing intermediate certificate (`Entrust OV TLS Issuing RSA CA 1`) needed for Anthem's certificate chain.

#### Option C: Temporary Workaround (Not Recommended for Production)
If you need an immediate fix and understand the security implications, you can temporarily disable SSL verification by updating `config.ini`:

```ini
[SSL]
VERIFY = true
DISABLE_VERIFICATION = true
```

**⚠️ WARNING: This disables SSL certificate verification and should only be used in controlled environments.**

## Testing the Fix

### 1. Check Certificate Status
```bash
# Test SSL connection to anthem.com
openssl s_client -connect mproducer.anthem.com:443 -servername mproducer.anthem.com
```

### 2. Verify Python SSL
```bash
# Test Python SSL configuration
python3 -c "import ssl; print(ssl.get_default_verify_paths())"
```

### 3. Application Testing
The application will now provide detailed SSL certificate loading information in the logs, showing which certificate strategy was successful.

## Production Deployment Steps

1. **Update the code** with the new SSL configuration
2. **Update system certificates** on the production server (Option A above)
3. **Restart the application**
4. **Monitor the logs** for SSL certificate loading messages
5. **Test the Anthem API connection**

## Log Messages to Look For

- `✓ Loaded default SSL certificates` - SSL is working correctly
- `✓ Configured SSL context with more permissive cipher settings` - SSL context optimized
- `✓ Configured SSL context with secure protocol options` - Secure protocols enabled
- `✓ Loaded certificates from /path/to/cert` - Using fallback certificate location
- `⚠ No SSL certificates found` - Need to update system certificates
- `⚠ WARNING: SSL verification is disabled` - SSL verification is disabled (not recommended)

## Success Indicators

When the fix is working correctly, you should see:
- **Status: 200** in application logs
- **Content-Type: application/json** in response headers
- **No SSL certificate verification errors**
- **Successful API responses** from Anthem

## Troubleshooting

If the issue persists:

1. **Check server certificate paths:**
   ```bash
   ls -la /etc/ssl/certs/
   ls -la /etc/pki/tls/certs/
   ```

2. **Verify certificate file permissions:**
   ```bash
   ls -la /etc/ssl/certs/ca-certificates.crt
   ```

3. **Test with curl:**
   ```bash
   curl -v https://mproducer.anthem.com
   ```

4. **Check Python SSL context:**
   ```python
   import ssl
   ctx = ssl.create_default_context()
   print(ctx.get_ca_certs())
   ```

## Security Notes

- Always prefer proper certificate installation over disabling SSL verification
- SSL verification should only be disabled in controlled, internal environments
- Regularly update system certificates to maintain security
- Monitor SSL connection logs for any certificate-related warnings
