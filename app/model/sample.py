"""Sample 도메인 객체"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Sample:
    """반도체 시료 도메인 모델"""
    id: str
    name: str
    avg_production_time: float
    yield_rate: float
    stock: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Sample:
        return cls(
            id=data["id"],
            name=data["name"],
            avg_production_time=float(data["avg_production_time"]),
            yield_rate=float(data["yield_rate"]),
            stock=int(data["stock"]),
        )
