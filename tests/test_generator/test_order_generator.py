"""Phase 3 - Red: OrderGenerator 테스트"""
import re
import pytest
from datetime import date

from app.generator.order_generator import OrderGenerator
from app.model.enums import OrderStatus

SAMPLE_IDS = ["S-001", "S-002", "S-003", "S-004", "S-005"]


@pytest.fixture
def generator():
    return OrderGenerator()


class TestOrderGenerator:
    def test_order_no_format(self, generator):
        """생성된 order_no가 ORD-\\d{8}-\\d{4} 형식을 준수한다."""
        order = generator.generate_one(
            sample_ids=SAMPLE_IDS,
            date=date(2026, 5, 8),
            seq=1,
        )
        assert re.fullmatch(r"ORD-\d{8}-\d{4}", order.order_no), \
            f"order_no '{order.order_no}'는 ORD-YYYYMMDD-XXXX 형식이 아닙니다"

    def test_order_no_date_encoded(self, generator):
        """order_no에 날짜가 올바르게 인코딩된다."""
        test_date = date(2026, 5, 8)
        order = generator.generate_one(
            sample_ids=SAMPLE_IDS,
            date=test_date,
            seq=1,
        )
        assert "20260508" in order.order_no

    def test_order_qty_positive(self, generator):
        """생성된 quantity가 양수(1 이상)다."""
        order = generator.generate_one(
            sample_ids=SAMPLE_IDS,
            date=date(2026, 5, 8),
            seq=1,
        )
        assert order.quantity > 0, f"quantity={order.quantity}는 양수가 아닙니다"

    def test_order_valid_status(self, generator):
        """생성된 status가 OrderStatus Enum 내 값이다."""
        order = generator.generate_one(
            sample_ids=SAMPLE_IDS,
            date=date(2026, 5, 8),
            seq=1,
        )
        assert isinstance(order.status, OrderStatus), \
            f"status '{order.status}'은 OrderStatus Enum이 아닙니다"
        assert order.status in list(OrderStatus)

    def test_order_status_fixed(self, generator):
        """status 인자를 직접 지정하면 해당 상태로 생성된다."""
        order = generator.generate_one(
            sample_ids=SAMPLE_IDS,
            date=date(2026, 5, 8),
            seq=1,
            status=OrderStatus.RESERVED,
        )
        assert order.status == OrderStatus.RESERVED

    def test_order_sample_id_in_pool(self, generator):
        """생성된 sample_id가 제공된 sample_ids 목록 내에 있다."""
        orders = generator.generate_many(sample_ids=SAMPLE_IDS, count=20)
        for o in orders:
            assert o.sample_id in SAMPLE_IDS, \
                f"sample_id '{o.sample_id}'는 sample_ids 목록에 없습니다"

    def test_order_no_duplicate(self, generator):
        """generate_many(20)으로 생성된 order_no 20개가 모두 유일하다."""
        orders = generator.generate_many(sample_ids=SAMPLE_IDS, count=20)
        order_nos = [o.order_no for o in orders]
        assert len(order_nos) == len(set(order_nos)), f"중복 order_no 발견: {order_nos}"

    def test_order_count(self, generator):
        """generate_many(n)은 정확히 n개를 반환한다."""
        for n in [1, 10, 20]:
            orders = generator.generate_many(sample_ids=SAMPLE_IDS, count=n)
            assert len(orders) == n, f"요청 {n}개이나 실제 {len(orders)}개"

    def test_order_base_date_default(self, generator):
        """base_date=None이면 오늘 날짜 기준으로 order_no를 생성한다."""
        today_str = date.today().strftime("%Y%m%d")
        orders = generator.generate_many(sample_ids=SAMPLE_IDS, count=3, base_date=None)
        for o in orders:
            assert today_str in o.order_no
