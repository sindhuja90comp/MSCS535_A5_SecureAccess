from app import create_app
from app.tls import ensure_self_signed_cert

app = create_app()

if __name__ == "__main__":
    cert_file, key_file = ensure_self_signed_cert("certs")
    app.run(host="0.0.0.0", port=5000, ssl_context=(cert_file, key_file))
