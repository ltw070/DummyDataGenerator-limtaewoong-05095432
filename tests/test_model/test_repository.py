"""Phase 1 Refactor: Repository CRUD 테스트 (커버리지 보강)"""
import pytest
from pathlib import Path

from app.repository.sample_repository import SampleRepository
from app.repository.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.order import Order
from app.model.enums import OrderStatus
from datetime import datetime


@pytest.fixture
def sample_repo(tmp_path: Path):
    return SampleRepository(file_path=tmp_path / "samples.json")


@pytest.fixture
def order_repo(tmp_path: Path):
    return OrderRepository(file_path=tmp_path / "orders.json")


@pytest.fixture
def sample():
    return Sample(id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=0.5, yield_rate=0.92, stock=100)


@pytest.fixture
def order():
    return Order(
        order_no="ORD-20260508-0001",
        sample_id="S-001",
        customer_name="삼성전자 파운드리",
        quantity=100,
        status=OrderStatus.RESERVED,
        created_at=datetime(2026, 5, 8),
    )


class TestSampleRepository:
    def test_save_and_find_by_id(self, sample_repo, sample):
        """저장 후 ID로 단건 조회된다."""
        sample_repo.save(sample)
        found = sample_repo.find_by_id("S-001")
        assert found is not None
        assert found.id == "S-001"

    def test_find_by_id_not_found(self, sample_repo):
        """존재하지 않는 ID 조회 시 None을 반환한다."""
        result = sample_repo.find_by_id("S-999")
        assert result is None

    def test_save_update(self, sample_repo, sample):
        """동일 ID로 저장 시 업데이트된다."""
        sample_repo.save(sample)
        updated = Sample(id="S-001", name="업데이트됨", avg_production_time=1.0, yield_rate=0.5, stock=0)
        sample_repo.save(updated)
        found = sample_repo.find_by_id("S-001")
        assert found.name == "업데이트됨"
        assert len(sample_repo.find_all()) == 1

    def test_delete(self, sample_repo, sample):
        """저장 후 삭제하면 find_all이 빈 리스트를 반환한다."""
        sample_repo.save(sample)
        result = sample_repo.delete("S-001")
        assert result is True
        assert sample_repo.find_all() == []

    def test_delete_not_found(self, sample_repo):
        """존재하지 않는 ID 삭제 시 False를 반환한다."""
        result = sample_repo.delete("S-999")
        assert result is False


class TestOrderRepository:
    def test_save_and_find_by_id(self, order_repo, order):
        """저장 후 order_no로 단건 조회된다."""
        order_repo.save(order)
        found = order_repo.find_by_id("ORD-20260508-0001")
        assert found is not None
        assert found.order_no == "ORD-20260508-0001"

    def test_find_by_id_not_found(self, order_repo):
        """존재하지 않는 order_no 조회 시 None을 반환한다."""
        result = order_repo.find_by_id("ORD-99999999-9999")
        assert result is None

    def test_save_update(self, order_repo, order):
        """동일 order_no로 저장 시 업데이트된다."""
        order_repo.save(order)
        updated = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-002",
            customer_name="SK하이닉스",
            quantity=200,
            status=OrderStatus.PRODUCING,
            created_at=datetime(2026, 5, 8),
        )
        order_repo.save(updated)
        found = order_repo.find_by_id("ORD-20260508-0001")
        assert found.quantity == 200
        assert len(order_repo.find_all()) == 1

    def test_delete(self, order_repo, order):
        """저장 후 삭제하면 find_all이 빈 리스트를 반환한다."""
        order_repo.save(order)
        result = order_repo.delete("ORD-20260508-0001")
        assert result is True
        assert order_repo.find_all() == []

    def test_delete_not_found(self, order_repo):
        """존재하지 않는 order_no 삭제 시 False를 반환한다."""
        result = order_repo.delete("ORD-99999999-9999")
        assert result is False
