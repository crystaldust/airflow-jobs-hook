import hashlib
import hmac
import os

GITHUB_WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET') or ''


def gen_signature(payload):
    digester = hmac.new(key=GITHUB_WEBHOOK_SECRET.encode('utf-8'),
                        msg=payload,
                        digestmod=hashlib.sha256)
    return digester.hexdigest()


async def validate_secret(req):
    header_signature = req.headers.get('X-Hub-Signature-256'.lower())
    if not header_signature:
        return False

    payload = await req.body()
    signature = gen_signature(payload)
    valid_signature = f'sha256={signature}'
    return header_signature == valid_signature


async def validate_sender(req):
    return True
