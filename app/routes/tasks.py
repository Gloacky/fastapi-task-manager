from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router=APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=list[schemas.Task])

def read_task(db:Session=Depends(get_db)):
    return db.query(models.Task).all()

@router.get("/{task_id}",response_model=schemas.Task)
def read_task(task_id: int, db: Session=Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found!")
    return task

@router.put("/{task_id}",response_model=schemas.Task)
def update_task(task_id:int,updated:schemas.TaskCreate, db:Session=Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title=updated.title
    task.description=updated.description
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db:Session=Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    
    db.delete(task)
    db.commit
    return{"detail":"Task deleted"}