"""Phase 4 - Red: Seeder 테스트"""
import pytest
from pathlib import Path

from app.generator.seeder import Seeder, SeedResult
from app.repository.sample_repository import SampleRepository
from app.repository.order_repository import OrderRepository


@pytest.fixture
def repos(tmp_path: Path):
    """임시 경로에 격리된 Sample/Order Repository를 생성한다."""
    sample_repo = SampleRepository(file_path=tmp_path / "samples.json")
    order_repo = OrderRepository(file_path=tmp_path / "orders.json")
    return sample_repo, order_repo


@pytest.fixture
def seeder(repos):
    sample_repo, order_repo = repos
    return Seeder(sample_repo=sample_repo, order_repo=order_repo)


class TestSeeder:
    def test_seeder_count(self, seeder, repos):
        """seed(5, 20) 후 repo에 Sample 5개, Order 20개가 저장된다."""
        sample_repo, order_repo = repos
        result = seeder.seed(sample_count=5, order_count=20)

        stored_samples = sample_repo.find_all()
        stored_orders = order_repo.find_all()

        assert len(stored_samples) == 5, f"Sample {len(stored_samples)}개 (기대: 5개)"
        assert len(stored_orders) == 20, f"Order {len(stored_orders)}개 (기대: 20개)"

    def test_seeder_result(self, seeder):
        """seed()는 SeedResult를 반환하며 생성 수량이 올바르다."""
        result = seeder.seed(sample_count=3, order_count=10)
        assert isinstance(result, SeedResult)
        assert result.samples_created == 3
        assert result.orders_created == 10

    def test_seeder_clear(self, seeder, repos):
        """seed 후 clear() 호출 시 find_all()이 빈 리스트를 반환한다."""
        sample_repo, order_repo = repos
        seeder.seed(sample_count=5, order_count=20)

        # 데이터가 존재함을 먼저 확인
        assert len(sample_repo.find_all()) == 5
        assert len(order_repo.find_all()) == 20

        seeder.clear()

        assert sample_repo.find_all() == [], "Sample clear 후 빈 리스트여야 합니다"
        assert order_repo.find_all() == [], "Order clear 후 빈 리스트여야 합니다"

    def test_seeder_default_count(self, seeder, repos):
        """seed()의 기본값은 sample=5, order=20이다."""
        sample_repo, order_repo = repos
        seeder.seed()

        assert len(sample_repo.find_all()) == 5
        assert len(order_repo.find_all()) == 20

    def test_seeder_sample_ids_used_in_orders(self, seeder, repos):
        """생성된 Order의 sample_id가 생성된 Sample id 목록 내에 있다."""
        sample_repo, order_repo = repos
        seeder.seed(sample_count=5, order_count=10)

        sample_ids = {s.id for s in sample_repo.find_all()}
        for order in order_repo.find_all():
            assert order.sample_id in sample_ids, \
                f"order.sample_id='{order.sample_id}' not in sample_ids={sample_ids}"

    def test_seeder_isolation(self, tmp_path: Path):
        """두 Seeder 인스턴스가 서로 다른 tmp_path를 사용하면 데이터가 격리된다."""
        path_a = tmp_path / "a"
        path_a.mkdir()
        path_b = tmp_path / "b"
        path_b.mkdir()

        seeder_a = Seeder(
            sample_repo=SampleRepository(path_a / "samples.json"),
            order_repo=OrderRepository(path_a / "orders.json"),
        )
        seeder_b = Seeder(
            sample_repo=SampleRepository(path_b / "samples.json"),
            order_repo=OrderRepository(path_b / "orders.json"),
        )

        seeder_a.seed(sample_count=2, order_count=5)
        seeder_b.seed(sample_count=3, order_count=7)

        assert len(seeder_a._sample_repo.find_all()) == 2
        assert len(seeder_b._sample_repo.find_all()) == 3
