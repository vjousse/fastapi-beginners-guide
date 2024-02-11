from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, DateTime, Integer, String, create_engine, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="app/templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

    created_at = Column(String, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __str__(self):
        return self.title


Base.metadata.create_all(bind=engine)


@app.get("/articles/create", include_in_schema=False)
async def articles_create(request: Request, db: Session = Depends(get_db)):
    article = Article(
        title="Mon titre de test", content="Un peu de contenu<br />avec deux lignes"
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    return templates.TemplateResponse(
        "articles_create.html", {"request": request, "article": article}
    )


@app.get("/articles", include_in_schema=False)
async def articles_list(request: Request, db: Session = Depends(get_db)):
    articles_statement = select(Article).order_by(Article.created_at)
    articles = db.scalars(articles_statement).all()

    return templates.TemplateResponse(
        "articles_list.html", {"request": request, "articles": articles}
    )


@app.get("/api/articles")
async def api_articles_list(db: Session = Depends(get_db)):
    articles_statement = select(Article).order_by(Article.created_at)

    return db.scalars(articles_statement).all()


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
