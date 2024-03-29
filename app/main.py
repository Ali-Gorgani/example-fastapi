# ------------------------- Libraries -------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)   # this part is now implemented by alembic and no need to run it.


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------- Routes -------------------------

@app.get('/')
def root():
    return {"message": "Hello World!"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
