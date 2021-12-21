import os

from fastapi import FastAPI, HTTPException, Request, status
from loguru import logger

from validators import validate_secret, validate_sender

validators = [validate_secret, validate_sender]
app = FastAPI()

LOG_FILEPATH = os.environ.get('LOG_FILEPATH') or './webhook.log'
print(LOG_FILEPATH)
logger.add(LOG_FILEPATH,
           format='[{level}]\t{name}:{function}:{line}\t{message}')


@app.post("/")
async def read_root_hook(req: Request):
    for validator in validators:
        is_valid = await validator(req)
        if not is_valid:
            logger.error(f'Failed to validate request: {validator.__name__}')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            return
    #  req_obj = await req.json()

    return {"Hello": "World"}
