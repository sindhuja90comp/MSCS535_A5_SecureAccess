from app import create_app
from app.tls import ensure_self_signed_cert

# Build the Flask app.
app = create_app()

if __name__ == "__main__":
    # Create certificate files if they do not exist yet.
    cert_file, key_file = ensure_self_signed_cert("certs")
    # Run the app over HTTPS so traffic is encrypted.
    app.run(host="0.0.0.0", port=5000, ssl_context=(cert_file, key_file))
