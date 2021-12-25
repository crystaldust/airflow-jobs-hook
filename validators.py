import hashlib
import hmac
from os import environ
from loguru import logger

GITHUB_WEBHOOK_SECRET = environ.get('GITHUB_WEBHOOK_SECRET') or ''
TARGET_BRANCH = environ.get('TARGET_BRANCH')


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


async def validate_branch(req):
    # When target branch not set, pull the default branch
    if not TARGET_BRANCH:
        return True

    payload = await req.json()
    logger.debug(payload)
    if 'ref' not in payload:
        logger.error('ref not in payload')
        return False

    ref = payload['ref']
    try:
        # A normal ref looks like this:
        # refs/heads/development
        branch = ref.split('/')[-1]
        return branch == TARGET_BRANCH
    except BaseException as e:
        logger.error(f'Failed to parse ref: {ref}, {type(e)}, {e}')
        return False
