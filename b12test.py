#!/usr/bin/env python3
"""
B12 Application Submission Script
Submits an application to https://b12.io/apply/submission with proper signing.
"""

import json
import hmac
import hashlib
import sys
import os
from datetime import datetime
from typing import Dict, Any
import urllib.request
import urllib.error


def get_iso8601_timestamp() -> str:
    """Get current timestamp in ISO 8601 format."""
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def create_payload(
    name: str,
    email: str,
    resume_link: str,
    repository_link: str,
    action_run_link: str,
    timestamp: str = None
) -> Dict[str, Any]:
    """Create the application payload with sorted keys."""
    if timestamp is None:
        timestamp = get_iso8601_timestamp()
    
    payload = {
        "action_run_link": action_run_link,
        "email": email,
        "name": name,
        "repository_link": repository_link,
        "resume_link": resume_link,
        "timestamp": timestamp,
    }
    
    return payload


def compute_signature(payload_json: str, secret: str = "hello-there-from-b12") -> str:
    """Compute HMAC-SHA256 signature for the payload."""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload_json.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


def serialize_payload(payload: Dict[str, Any]) -> str:
    """Serialize payload to compact JSON with sorted keys and no extra whitespace."""
    return json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def submit_application(
    name: str,
    email: str,
    resume_link: str,
    repository_link: str,
    action_run_link: str
) -> Dict[str, Any]:
    """Submit application to B12."""
    
    # Create payload
    payload = create_payload(name, email, resume_link, repository_link, action_run_link)
    payload_json = serialize_payload(payload)
    
    # Compute signature
    signature = compute_signature(payload_json)
    
    # Prepare request
    url = "https://b12.io/apply/submission"
    
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('X-Signature-256', signature)
    req.data = payload_json.encode('utf-8')
    
    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            response_json = json.loads(response_data)
            
            if response.status == 200:
                print(f"✓ Application submitted successfully!")
                if 'receipt' in response_json:
                    print(f"Receipt: {response_json['receipt']}")
                    return response_json
                else:
                    print(f"Response: {response_json}")
                    return response_json
            else:
                print(f"✗ Unexpected status code: {response.status}")
                print(f"Response: {response_json}")
                return None
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"✗ HTTP Error {e.code}: {error_body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗ Network Error: {e.reason}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse response: {e}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    
    # Get values from environment variables or command-line arguments
    name = os.getenv('B12_NAME') or (sys.argv[1] if len(sys.argv) > 1 else None)
    email = os.getenv('B12_EMAIL') or (sys.argv[2] if len(sys.argv) > 2 else None)
    resume_link = os.getenv('B12_RESUME_LINK') or (sys.argv[3] if len(sys.argv) > 3 else None)
    repository_link = os.getenv('B12_REPOSITORY_LINK') or (sys.argv[4] if len(sys.argv) > 4 else None)
    action_run_link = os.getenv('B12_ACTION_RUN_LINK') or (sys.argv[5] if len(sys.argv) > 5 else None)
    
    # Validate required fields
    required_fields = {
        'name': name,
        'email': email,
        'resume_link': resume_link,
        'repository_link': repository_link,
        'action_run_link': action_run_link,
    }
    
    missing_fields = [k for k, v in required_fields.items() if not v]
    
    if missing_fields:
        print(f"✗ Missing required fields: {', '.join(missing_fields)}")
        print("\nUsage (command-line arguments):")
        print(f"  python {sys.argv[0]} <name> <email> <resume_link> <repository_link> <action_run_link>")
        print("\nOr set environment variables:")
        for field in required_fields.keys():
            print(f"  B12_{field.upper()}")
        sys.exit(1)
    
    # Submit application
    result = submit_application(name, email, resume_link, repository_link, action_run_link)
    
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
