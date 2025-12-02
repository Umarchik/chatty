from app.application.dto.account_dto import AccountResponseDTO, CreateAccountDTO
from app.domain.entities.account import Account


class AccountMapper:
    @staticmethod
    def create_dto_to_entity(dto: CreateAccountDTO) -> Account:
        return Account(
            email=dto.email,
            phone=dto.phone,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )

    @staticmethod
    def create_to_response_dto(entity: Account) -> AccountResponseDTO:
        return AccountResponseDTO(
            id=entity.id,
            email=entity.email,
            phone=entity.phone,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at,
        )
    