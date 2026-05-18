import uvicorn
from fastapi import FastAPI

from db.crud.crud import crud_router

DEBUG = True
app = FastAPI()

app.include_router(crud_router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/inventory", response_model=List[Inventory])
# async def inventory(code:Annotated[List[str] | None, Query()] = None,
#                     name:Annotated[List[str] | None, Query()] = None) -> Any:
#     if code and name:
#         raise HTTPException(status_code=400, detail="only one of the query parametes should be used")
#     elif code or name:
#         if code:
#             data = read(key='code',
#                         values=code) #going to filter out the resutls based on the
#                                                                        # code or name provided
#         elif name:
#             data = read(key='name',
#                         values=name)
#         return data
#     else:
#         data = read()
#         return data

# class test_depended():
#     def __init__(self, p=10, a='a', b='b'):
#         self.p = p
#         self.a = a
#         self.b = b
#
# @app.get("/dependency-test")
# async def test_endpoint(common: Annotated[test_depended, Depends(test_depended)]):
#     return common


if DEBUG:
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
