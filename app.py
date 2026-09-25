#!/usr/bin/env python3
"""
File Integrity Checker — Web Application Entrypoint.
Delegates application lifecycle and routes to modular core and web packages.
"""

import os
import sys
from web.server import create_app

def main():
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("DEBUG", "false").lower() == "true"

    banner = r"""
  ===============================================================
     __ _ _        ___       _                  _ _           
    / _(_) |      |_ _|     | |                (_) |          
   | |_ _| | ___   | | _ __ | |_ ___  __ _ _ __ _| |_ _   _   
   |  _| | |/ _ \  | || '_ \| __/ _ \/ _` | '__| | __| | | |  
   | | | | |  __/ _| || | | | ||  __/ (_| | |  | | |_| |_| |  
   |_| |_|_|\___||___|_| |_|\__\___|\__, |_|  |_|\__|\__, |  
                                     __/ |            __/ |  
                                    |___/            |___/   
                     Cryptographic Verification Utility
  ===============================================================
    """
    print(banner)
    print(f" [*] Local Server URL : http://{host}:{port}")
    print(f" [*] Storage Database  : integrity_checker.db")
    print(f" [*] SHA-256 Engine   : Python hashlib (Streaming 64KB buffers)")
    print(f" [*] Mode              : Local & Privacy-Preserving")
    print(" ---------------------------------------------------------------")
    print(" Press Ctrl+C to terminate.")

    app = create_app()
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()
