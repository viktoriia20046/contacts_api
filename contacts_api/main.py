from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db  # Перевірте правильність шляху
import models  # Замініть відносні імпорти на абсолютні
import schemas  # Замініть відносні імпорти на абсолютні

app = FastAPI()

# Приклад маршруту для створення контакту
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    new_contact = models.Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# Приклад маршруту для отримання всіх контактів
@app.get("/contacts/", response_model=list[schemas.Contact])
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

# Приклад маршруту для отримання контакту за ID
@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return contact

# Приклад маршруту для оновлення контакту
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, updated_contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    for key, value in updated_contact.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact

# Приклад маршруту для видалення контакту
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    db.delete(contact)
    db.commit()
    return {"detail": "Контакт успішно видалено"}

# Приклад маршруту для отримання контактів з найближчими днями народження
from datetime import date, timedelta

@app.get("/contacts/upcoming_birthdays/", response_model=list[schemas.Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    upcoming = today + timedelta(days=7)
    contacts = db.query(models.Contact).filter(models.Contact.birthday.between(today, upcoming)).all()
    return contacts