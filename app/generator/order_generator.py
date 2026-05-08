"""OrderGenerator - Order Dummy 데이터 생성기"""
from __future__ import annotations
import random
from datetime import date, datetime

from app.model.order import Order
from app.model.enums import OrderStatus

CUSTOMER_POOL = [
    "삼성전자 파운드리",
    "SK하이닉스",
    "LG이노텍",
    "DB하이텍",
    "매그나칩",
    "키파운드리",
]

_ALL_STATUSES = list(OrderStatus)


class OrderGenerator:
    """도메인 규칙을 준수하는 Order Dummy 데이터 생성기"""

    CUSTOMER_POOL = CUSTOMER_POOL

    def generate_one(
        self,
        sample_ids: list[str],
        date: date,
        seq: int,
        status: OrderStatus | None = None,
    ) -> Order:
        """seq를 받아 유효한 Order 하나를 생성한다.

        order_no 형식: "ORD-{YYYYMMDD}-{seq:04d}"  예: ORD-20260508-0001
        status가 None이면 OrderStatus 전체에서 랜덤 선택 (REJECTED 포함).
        """
        order_no = f"ORD-{date.strftime('%Y%m%d')}-{seq:04d}"
        chosen_status = status if status is not None else random.choice(_ALL_STATUSES)
        return Order(
            order_no=order_no,
            sample_id=random.choice(sample_ids),
            customer_name=random.choice(self.CUSTOMER_POOL),
            quantity=random.randint(1, 500),
            status=chosen_status,
            created_at=datetime.combine(date, datetime.min.time()),
        )

    def generate_many(
        self,
        sample_ids: list[str],
        count: int,
        base_date: date | None = None,
    ) -> list[Order]:
        """count개의 Order를 생성한다. order_no 중복 없음을 보장한다.

        base_date가 None이면 오늘 날짜 사용.
        seq를 1부터 순차 증가시켜 ORD-YYYYMMDD-0001, 0002, ... 형식으로 고유 order_no 보장.
        """
        target_date = base_date if base_date is not None else date.today()
        return [self.generate_one(sample_ids=sample_ids, date=target_date, seq=i) for i in range(1, count + 1)]
