from pathlib import Path
from ipaddress import ip_address
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization

def ensure_self_signed_cert(cert_dir: str):
    # Store the certificate files in the chosen folder.
    cert_dir_path = Path(cert_dir)
    cert_dir_path.mkdir(parents=True, exist_ok=True)
    cert_file = cert_dir_path / "server.crt"
    key_file = cert_dir_path / "server.key"

    # Reuse existing files so a new certificate is not created every time.
    if cert_file.exists() and key_file.exists():
        return str(cert_file), str(key_file)

    # Create a new private key for HTTPS.
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Texas"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Dallas"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SecureAccess"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    # Add the local names and IP address that the certificate should trust.
    san = x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.DNSName("127.0.0.1"),
        x509.IPAddress(ip_address("127.0.0.1")),
    ])

    # Build and sign a self-signed certificate.
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc) - timedelta(minutes=1))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
        .add_extension(san, critical=False)
        .sign(key, hashes.SHA256())
    )

    # Save the private key and certificate to disk.
    key_file.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    cert_file.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    return str(cert_file), str(key_file)
