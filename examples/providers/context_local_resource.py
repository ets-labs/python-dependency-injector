from uuid import uuid4

from fastapi import Depends, FastAPI

from dependency_injector import containers, providers
from dependency_injector.wiring import Closing, Provide, inject

global_list = []


class AsyncSessionLocal:
    def __init__(self):
        self.id = uuid4()

    async def __aenter__(self):
        print("Entering session !")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing session !")

    async def execute(self, user_input):
        return f"Executing {user_input} in session {self.id}"


app = FastAPI()


class Container(containers.DeclarativeContainer):
    db_session = providers.ContextLocalResource(AsyncSessionLocal)


@app.get("/")
@inject
async def index(db: AsyncSessionLocal = Depends(Closing[Provide["db_session"]])):
    if db.id in global_list:
        raise Exception("The db session was already used")  # never reaches here
    global_list.append(db.id)
    res = await db.execute("SELECT 1")
    return str(res)


if __name__ == "__main__":
    import uvicorn

    container = Container()
    container.wire(modules=["__main__"])
    uvicorn.run(app, host="localhost", port=8000)
    container.unwire()
