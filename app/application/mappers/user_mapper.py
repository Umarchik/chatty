from datetime import datetime
from typing import Optional
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.domain.entities.user import User


class UserMapper:
    @staticmethod
    def create_dto_to_entity(dto: CreateUserDTO, account_id: Optional[int]=None) -> User:
        final_account_id = account_id if account_id is not None else dto.account_id

        if final_account_id is None:
            raise ValueError("account_id must be provided either in DTO or as parameter")
        
        return User(
            
            external_id=dto.external_id,
            messenger_type=dto.messenger_type,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
            account_id=account_id,
            created_at = datetime.utcnow()
        )
    
    @classmethod
    def create_to_response_dto(entity: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=entity.id,
            external_id=entity.external_id,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            account_id=entity.account_id,
            created_at=entity.created_at,            
        )
    