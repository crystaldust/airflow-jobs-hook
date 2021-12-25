import shutil
from os import environ, path

from fastapi import FastAPI, HTTPException, Request, status
from git import Git, Repo
from loguru import logger

from validators import validate_secret, validate_sender

validators = [validate_secret, validate_sender]
app = FastAPI()

LOG_FILEPATH = environ.get('LOG_FILEPATH')
if LOG_FILEPATH:
    logger.add(
        LOG_FILEPATH,
        format='[{level}]\t{name}:{function}:{line}\t{message}',
    )

GIT_REPOPATH = environ.get('GIT_REPOPATH') or '/tmp/airflow-jobs-repo'
GIT_REPO_URL = environ.get(
    'GIT_REPO_URL', ) or 'https://github.com/fivestarsky/airflow-jobs'
AIRFLOW_DAGS_PATH = environ.get(
    'AIRFLOW_DAGS_PATH', ) or '/mnt/nfs4_share/airflow-pvs/dags'


@app.post("/")
async def read_root_hook(req: Request):
    for validator in validators:
        if not await validator(req):
            logger.error(f'Failed to validate request: {validator.__name__}')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            return

    repo = None
    if path.exists(GIT_REPOPATH):
        repo = Repo(GIT_REPOPATH)
        logger.info(f'{GIT_REPOPATH} already there')
    else:
        repo = Repo.clone_from(GIT_REPO_URL, GIT_REPOPATH)

    origin = repo.remote('origin')
    origin.pull()
    # TODO shutil doesn't provide 'overwrite' features for now
    shutil.copytree(
        f'{GIT_REPOPATH}/dags',
        AIRFLOW_DAGS_PATH,
        dirs_exist_ok=True,
    )
    return ""
