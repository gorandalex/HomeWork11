from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import and_, or_, func, text
from sqlalchemy.orm import Session

from src.models.contacts import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session) -> List[Contact]:
    owners = db.query(Contact).all()
    return owners


async def get_contact(contact_id: int, db: Session) -> Contact:
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session) -> Contact:
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def delete_contact(contact_id: int, db: Session) -> Contact:
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contact(
        db: Session,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
) -> List[Contact]:
    contact = db.query(Contact).filter(
        and_(
            or_(Contact.first_name == first_name, first_name is None),
            or_(Contact.last_name == last_name, last_name is None),
            or_(Contact.email == email, email is None),
        )
    ).all()

    return contact


async def search_birthday_contact(db: Session) -> List[Contact]:
    date_from = date.today()
    date_to = date.today() + timedelta(days=7)
    this_year = date_from.year
    next_year = date_from.year + 1
    contact = db.query(Contact).filter(
        or_(
            func.to_date(func.concat(func.to_char(Contact.birthday, "DDMM"), this_year), "DDMMYYYY").between(date_from,
                                                                                                             date_to),
            func.to_date(func.concat(func.to_char(Contact.birthday, "DDMM"), next_year), "DDMMYYYY").between(date_from,
                                                                                                             date_to),
        )
    ).all()

    return contact
