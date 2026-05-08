"""Seeder - 저장소 삽입 오케스트레이터"""
from __future__ import annotations
from dataclasses import dataclass

from app.generator.sample_generator import SampleGenerator
from app.generator.order_generator import OrderGenerator
from app.repository.sample_repository import SampleRepository
from app.repository.order_repository import OrderRepository


@dataclass
class SeedResult:
    """Seeder 실행 결과"""
    samples_created: int
    orders_created: int


class Seeder:
    """Sample과 Order Dummy 데이터를 생성하여 저장소에 삽입하는 오케스트레이터"""

    def __init__(
        self,
        sample_repo: SampleRepository,
        order_repo: OrderRepository,
    ) -> None:
        self._sample_repo = sample_repo
        self._order_repo = order_repo
        self._sample_gen = SampleGenerator()
        self._order_gen = OrderGenerator()

    def seed(self, sample_count: int = 5, order_count: int = 20) -> SeedResult:
        """sample_count개 Sample, order_count개 Order를 생성하여 저장소에 삽입한다.

        1. sample_count개 Sample 생성 → sample_repo에 저장
        2. order_count개 Order 생성 (sample id 참조) → order_repo에 저장
        3. SeedResult 반환
        """
        samples = self._sample_gen.generate_many(count=sample_count)
        for sample in samples:
            self._sample_repo.save(sample)

        sample_ids = [s.id for s in samples]
        orders = self._order_gen.generate_many(sample_ids=sample_ids, count=order_count)
        for order in orders:
            self._order_repo.save(order)

        return SeedResult(
            samples_created=sample_count,
            orders_created=order_count,
        )

    def clear(self) -> None:
        """저장소 전체 데이터를 삭제한다."""
        self._sample_repo.delete_all()
        self._order_repo.delete_all()
