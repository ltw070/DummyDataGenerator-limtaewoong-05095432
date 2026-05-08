"""SampleGenerator - Sample Dummy 데이터 생성기"""
from __future__ import annotations
import random

from app.model.sample import Sample

# (name, avg_production_time, yield_rate)
SAMPLE_POOL = [
    ("실리콘 웨이퍼-8인치", 0.5, 0.92),
    ("GaN 에피택셜-4인치", 0.3, 0.78),
    ("SiC 파워기판-6인치", 0.8, 0.92),
    ("포토레지스트-PR7", 0.2, 0.95),
    ("산화막 웨이퍼-SiO2", 0.6, 0.88),
]


class SampleGenerator:
    """도메인 규칙을 준수하는 Sample Dummy 데이터 생성기"""

    SAMPLE_POOL = SAMPLE_POOL

    def generate_one(self, index: int) -> Sample:
        """index를 받아 유효한 Sample 하나를 생성한다.

        id 형식: "S-{index:03d}"  예: S-001, S-012
        SAMPLE_POOL에서 순환하여 name, avg_production_time, yield_rate 선택.
        stock은 0~999 사이 랜덤 정수.
        """
        pool_item = self.SAMPLE_POOL[(index - 1) % len(self.SAMPLE_POOL)]
        name, avg_production_time, yield_rate = pool_item
        return Sample(
            id=f"S-{index:03d}",
            name=name,
            avg_production_time=avg_production_time,
            yield_rate=yield_rate,
            stock=random.randint(0, 999),
        )

    def generate_many(self, count: int) -> list[Sample]:
        """count개의 Sample을 생성한다. id 중복 없음을 보장한다.

        index를 1부터 순차 증가시켜 S-001, S-002, ... 형식으로 고유 id 보장.
        """
        return [self.generate_one(index=i) for i in range(1, count + 1)]
