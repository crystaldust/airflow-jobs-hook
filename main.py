from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/payload")
async def read_payload(req: Request):
    req_obj = await req.json()
    return {"Hello": "World"}
