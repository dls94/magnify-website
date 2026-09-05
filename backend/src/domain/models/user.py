from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4


class UserRole(str, Enum):
    ADMIN = "ADMIN"


@dataclass
class User:
    email: str
    password_hash: str
    role: UserRole = UserRole.ADMIN
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def __post_init__(self) -> None:
        if not self.email or not self.email.strip():
            raise ValueError("L'email est obligatoire.")

        if "@" not in self.email:
            raise ValueError("L'email est invalide.")

        if not self.password_hash:
            raise ValueError("Le mot de passe hashé est obligatoire.")

    def deactivate(self) -> None:
        if not self.is_active:
            raise ValueError("L'utilisateur est déjà désactivé.")

        self.is_active = False

    def activate(self) -> None:
        if self.is_active:
            raise ValueError("L'utilisateur est déjà actif.")

        self.is_active = True