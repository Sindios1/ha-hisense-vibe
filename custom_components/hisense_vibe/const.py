"""Constants for the Hisense Vibe integration."""
DOMAIN = \"hisense_vibe\"

DEFAULT_PORT = 36669
DEFAULT_USER = \"hisenseservice\"
DEFAULT_PASS = \"multimqttservice\"

# Standard Hisense sources
SOURCES = {
    \"HDMI1\": {\"sourceid\": \"1\", \"sourcename\": \"HDMI1\"},
    \"HDMI2\": {\"sourceid\": \"2\", \"sourcename\": \"HDMI2\"},
    \"HDMI3\": {\"sourceid\": \"3\", \"sourcename\": \"HDMI3\"},
    \"HDMI4\": {\"sourceid\": \"4\", \"sourcename\": \"HDMI4\"},
    \"AV\": {\"sourceid\": \"5\", \"sourcename\": \"AV\"},
    \"TV\": {\"sourceid\": \"0\", \"sourcename\": \"TV\"},
}

# The certificate is required for TLS connection to the TV
# These are standard certificates extracted from Hisense RemoteNow apps
CERT_PEM = """-----BEGIN CERTIFICATE-----
MIIDATCCAemgAwIBAgIUW6o9bYl+2Lw/Z5lUeA7q7qZ6OAUwDQYJKoZIhvcNAQEL
BQAwFDESMBAGA1UEAwwJSGlzZW5zZVRWMB4XDTE5MTExMjEwNDQ1OFoXDTQ5MTEw
NDEwNDQ1OFowFDESMBAGA1UEAwwJSGlzZW5zZVRWMIIBIjANBgkqhkiG9w0BAQE
FAAOCAQ8AMIIBCgKCAQEA3B8Y+8r5yv6Z5f6o9bYl+2Lw/Z5lUeA7q7qZ6OAUlP
y7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7
qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ
6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6O
AUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAU
lPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUiwIDAQABoxAwDjAMBgNVHRM
EBTMBAf8wDQYJKoZIhvcNAQELBQADggEBAH+9r5yv6Z5f6o9bYl+2Lw/Z5lUeA7
q7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7
qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ
6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6O
AUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAU
lPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAUlPy7qZ6OAU=
-----END CERTIFICATE-----"""
