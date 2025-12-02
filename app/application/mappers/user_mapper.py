from typing import Optional
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.domain.entities.user import User


class UserMapper:

    @staticmethod
    def from_create_dto(dto: CreateUserDTO, account_id: Optional[int] = None) -> User:
        """Преобразование DTO -> Entity"""

        # Определяем account_id
        final_account_id = account_id if account_id is not None else dto.account_id
        if final_account_id is None:
            raise ValueError("account_id must be provided either in DTO or as parameter")

        return User(
            external_id=dto.external_id,
            #messenger_type=dto.messenger_type.value,   # <-- важно!
            messenger_type=dto.messenger_type,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
            account_id=final_account_id,
            # created_at НЕ задаём — это делает SQLAlchemy
        )

    @staticmethod
    def to_response_dto(entity: User) -> UserResponseDTO:
        """Преобразование Entity -> DTO ответа"""

        return UserResponseDTO(
            id=entity.id,
            external_id=entity.external_id,
            messenger_type=entity.messenger_type,   # <-- добавили!
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            account_id=entity.account_id,
            created_at=entity.created_at,
        )
