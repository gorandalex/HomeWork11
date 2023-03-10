from typing import List, Optional

from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contact

from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/search", response_model=List[ContactResponse])
async def search_contact(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        db: Session = Depends(get_db),
        owner_id: Optional[int] = Depends(auth_service.get_current_user),
):
    contact = await repository_contact.search_contact(first_name=first_name, last_name=last_name, email=email, db=db, owner_id=owner_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/birthday", response_model=List[ContactResponse])
async def birthday_contact(db: Session = Depends(get_db), owner_id: Optional[int] = Depends(auth_service.get_current_user)):
    contact = await repository_contact.search_birthday_contact(db, owner_id=owner_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db), owner_id: Optional[int] = Depends(auth_service.get_current_user)):
    contacts = await repository_contact.get_contacts(db, owner_id=owner_id)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, status_code=status.HTTP_404_NOT_FOUND)
async def get_contact(
        contact_id: int = Path(1, ge=1),
        owner_id: Optional[int] = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
) -> ContactModel:
    contact = await repository_contact.get_contact(contact_id, db, owner_id=owner_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contact.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_404_NOT_FOUND)
async def update_contact(body: ContactModel, contact_id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    contact = await repository_contact.update_owner(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(1, ge=1), db: Session = Depends(get_db), owner_id: Optional[int] = Depends(auth_service.get_current_user)):
    contact = await repository_contact.delete_owner(contact_id, db, owner_id=owner_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
