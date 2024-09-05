import fastapi
from fastapi import HTTPException
import database
import contacts.schema as schema
import contacts.model as model
from datetime import datetime, timedelta

router = fastapi.APIRouter(prefix="/contacts", tags=["Contacts"])

@router.get("/")
async def root(
    db=fastapi.Depends(database.get_database)
)-> list[model.ContactResponse]:
    return [contact for contact in db.query(schema.Contacts).all()]

@router.get("/find/{contact_id}")
async def get_by_id(contact_id : int,
    db=fastapi.Depends(database.get_database)
)->model.ContactResponse:
    contact = db.query(schema.Contacts).filter(schema.Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.post("/")
async def post_root(
    contact: model.ContactModel,
    db=fastapi.Depends(database.get_database)
)-> model.ContactModel:
    new_contact = schema.Contacts(**contact.__dict__)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact

@router.delete("/{contact_id}")
async def del_by_id(contact_id : int,   
    db=fastapi.Depends(database.get_database)
):
    contact = db.query(schema.Contacts).filter(schema.Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}

@router.patch("/{contact_id}")
async def patch_contact(contact_id:int,
    contact_data: model.ContactUpdate,
    db=fastapi.Depends(database.get_database)
) -> model.ContactResponse:
    contact = db.query(schema.Contacts).filter(schema.Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in contact_data.dict(exclude_unset=True).items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact

@router.get("/search")
async def search_contacts(
    name: str = None,
    surename: str = None,
    email: str = None,
    db=fastapi.Depends(database.get_database)
) -> list[model.ContactResponse]:
    query = db.query(schema.Contacts)
    
    if name:
        query = query.filter(schema.Contacts.name == name)
    if surename:
        query = query.filter(schema.Contacts.surename == surename)
    if email:
        query = query.filter(schema.Contacts.email == email)
    
    results = query.all()
    return results

@router.get("/upcoming-birthdays")
async def get_upcoming_birthdays(
    db=fastapi.Depends(database.get_database)
)-> list[model.ContactResponse]:
    today = datetime.today().date()
    upcoming_date = datetime.today().date() + timedelta(days=7)

    contacts_with_upcoming_birthdays = db.query(schema.Contacts).filter(
        schema.Contacts.date_of_birth.between(today, upcoming_date)
    ).all()

    return contacts_with_upcoming_birthdays