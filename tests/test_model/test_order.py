"""Phase 1 - Red: Order 도메인 모델 테스트"""
import pytest
from datetime import datetime
from app.model.order import Order
from app.model.enums import OrderStatus


class TestOrderStatus:
    def test_order_status_values(self):
        """OrderStatus Enum에 필요한 값이 정의되어 있다."""
        assert OrderStatus.RESERVED
        assert OrderStatus.PRODUCING
        assert OrderStatus.CONFIRMED
        assert OrderStatus.RELEASE
        assert OrderStatus.REJECTED

    def test_order_status_flow(self):
        """상태 흐름 값이 문자열로 표현 가능하다."""
        assert OrderStatus.RESERVED.value == "RESERVED"
        assert OrderStatus.PRODUCING.value == "PRODUCING"
        assert OrderStatus.CONFIRMED.value == "CONFIRMED"
        assert OrderStatus.RELEASE.value == "RELEASE"
        assert OrderStatus.REJECTED.value == "REJECTED"


class TestOrder:
    def test_order_creation(self):
        """Order 객체가 올바르게 생성된다."""
        order = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="삼성전자 파운드리",
            quantity=100,
            status=OrderStatus.RESERVED,
            created_at=datetime(2026, 5, 8),
        )
        assert order.order_no == "ORD-20260508-0001"
        assert order.sample_id == "S-001"
        assert order.customer_name == "삼성전자 파운드리"
        assert order.quantity == 100
        assert order.status == OrderStatus.RESERVED

    def test_order_field_types(self):
        """Order 필드 타입이 올바르다."""
        order = Order(
            order_no="ORD-20260508-0002",
            sample_id="S-002",
            customer_name="SK하이닉스",
            quantity=50,
            status=OrderStatus.PRODUCING,
            created_at=datetime(2026, 5, 8),
        )
        assert isinstance(order.order_no, str)
        assert isinstance(order.sample_id, str)
        assert isinstance(order.customer_name, str)
        assert isinstance(order.quantity, int)
        assert isinstance(order.status, OrderStatus)

    def test_order_to_dict(self):
        """Order를 dict로 직렬화할 수 있다."""
        order = Order(
            order_no="ORD-20260508-0003",
            sample_id="S-003",
            customer_name="LG이노텍",
            quantity=30,
            status=OrderStatus.CONFIRMED,
            created_at=datetime(2026, 5, 8),
        )
        data = order.to_dict()
        assert data["order_no"] == "ORD-20260508-0003"
        assert data["status"] == "CONFIRMED"

    def test_order_from_dict(self):
        """dict에서 Order를 역직렬화할 수 있다."""
        data = {
            "order_no": "ORD-20260508-0004",
            "sample_id": "S-004",
            "customer_name": "DB하이텍",
            "quantity": 20,
            "status": "RESERVED",
            "created_at": "2026-05-08T00:00:00",
        }
        order = Order.from_dict(data)
        assert order.order_no == "ORD-20260508-0004"
        assert order.status == OrderStatus.RESERVED
