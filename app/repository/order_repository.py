"""OrderRepository - JSON 파일 기반 구현"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

from app.model.order import Order
from app.repository.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Order 데이터를 JSON 파일에 저장하는 구현체"""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._write([])

    def _read(self) -> list[dict]:
        with self._file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: list[dict]) -> None:
        with self._file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, entity: Order) -> Order:
        records = self._read()
        existing = next((i for i, r in enumerate(records) if r["order_no"] == entity.order_no), None)
        if existing is not None:
            records[existing] = entity.to_dict()
        else:
            records.append(entity.to_dict())
        self._write(records)
        return entity

    def find_by_id(self, id: str) -> Optional[Order]:
        records = self._read()
        for record in records:
            if record["order_no"] == id:
                return Order.from_dict(record)
        return None

    def find_all(self) -> list[Order]:
        records = self._read()
        return [Order.from_dict(r) for r in records]

    def delete(self, id: str) -> bool:
        records = self._read()
        filtered = [r for r in records if r["order_no"] != id]
        if len(filtered) == len(records):
            return False
        self._write(filtered)
        return True

    def delete_all(self) -> None:
        self._write([])
