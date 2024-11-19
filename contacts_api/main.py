from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Contact
from database import get_db
from database import Base # Абсолютний імпорт
import models  # Абсолютний імпорт
import schemas  # Абсолютний імпорт

app = FastAPI()

# Приклад маршруту для отримання всіх контактів
@app.get("/contacts", response_model=list[schemas.Contact])
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

# Приклад маршруту для створення нового контакту
@app.post("/contacts", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    new_contact = models.Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# Приклад маршруту для оновлення контакту
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, updated_contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    for key, value in updated_contact.dict(exclude_unset=True).items():
        setattr(contact, key, value)
    
    db.commit()
    db.refresh(contact)
    return contact

# Приклад маршруту для видалення контакту
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}