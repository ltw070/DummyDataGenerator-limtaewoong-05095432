"""SampleRepository - JSON 파일 기반 구현"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

from app.model.sample import Sample
from app.repository.base_repository import BaseRepository


class SampleRepository(BaseRepository[Sample]):
    """Sample 데이터를 JSON 파일에 저장하는 구현체"""

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

    def save(self, entity: Sample) -> Sample:
        records = self._read()
        existing = next((i for i, r in enumerate(records) if r["id"] == entity.id), None)
        if existing is not None:
            records[existing] = entity.to_dict()
        else:
            records.append(entity.to_dict())
        self._write(records)
        return entity

    def find_by_id(self, id: str) -> Optional[Sample]:
        records = self._read()
        for record in records:
            if record["id"] == id:
                return Sample.from_dict(record)
        return None

    def find_all(self) -> list[Sample]:
        records = self._read()
        return [Sample.from_dict(r) for r in records]

    def delete(self, id: str) -> bool:
        records = self._read()
        filtered = [r for r in records if r["id"] != id]
        if len(filtered) == len(records):
            return False
        self._write(filtered)
        return True

    def delete_all(self) -> None:
        self._write([])
