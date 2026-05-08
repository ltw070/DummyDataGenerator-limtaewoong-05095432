"""BaseRepository 추상 인터페이스"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """CRUD 추상 인터페이스"""

    @abstractmethod
    def save(self, entity: T) -> T:
        """엔티티 저장 (신규/수정)"""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """ID로 단건 조회"""

    @abstractmethod
    def find_all(self) -> list[T]:
        """전체 목록 조회"""

    @abstractmethod
    def delete(self, id: str) -> bool:
        """ID로 삭제"""

    @abstractmethod
    def delete_all(self) -> None:
        """전체 삭제"""
