"""Order 도메인 객체"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.model.enums import OrderStatus


@dataclass
class Order:
    """생산 주문 도메인 모델"""
    order_no: str
    sample_id: str
    customer_name: str
    quantity: int
    status: OrderStatus
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_no": self.order_no,
            "sample_id": self.sample_id,
            "customer_name": self.customer_name,
            "quantity": self.quantity,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Order:
        return cls(
            order_no=data["order_no"],
            sample_id=data["sample_id"],
            customer_name=data["customer_name"],
            quantity=int(data["quantity"]),
            status=OrderStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
