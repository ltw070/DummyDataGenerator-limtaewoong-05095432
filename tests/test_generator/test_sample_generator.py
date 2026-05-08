"""Phase 2 - Red: SampleGenerator 테스트"""
import re
import pytest
from app.generator.sample_generator import SampleGenerator


@pytest.fixture
def generator():
    return SampleGenerator()


class TestSampleGenerator:
    def test_sample_id_format(self, generator):
        """생성된 id가 S-\\d{3} 형식을 준수한다."""
        sample = generator.generate_one(index=1)
        assert re.fullmatch(r"S-\d{3}", sample.id), f"id '{sample.id}'는 S-XXX 형식이 아닙니다"

    def test_sample_id_format_multiple(self, generator):
        """여러 인덱스에서 생성된 id가 모두 S-\\d{3} 형식을 준수한다."""
        for i in range(1, 6):
            sample = generator.generate_one(index=i)
            assert re.fullmatch(r"S-\d{3}", sample.id), f"index={i}에서 id '{sample.id}' 형식 오류"

    def test_sample_yield_range(self, generator):
        """생성된 yield_rate가 0 초과 1 이하다."""
        sample = generator.generate_one(index=1)
        assert 0 < sample.yield_rate <= 1, f"yield_rate={sample.yield_rate}는 범위 초과"

    def test_sample_yield_range_many(self, generator):
        """generate_many로 생성된 모든 샘플의 yield_rate가 유효하다."""
        samples = generator.generate_many(count=10)
        for s in samples:
            assert 0 < s.yield_rate <= 1, f"yield_rate={s.yield_rate}는 범위 초과"

    def test_sample_production_time_positive(self, generator):
        """avg_production_time이 양수다."""
        sample = generator.generate_one(index=1)
        assert sample.avg_production_time > 0

    def test_sample_stock_non_negative(self, generator):
        """stock이 0 이상 999 이하의 정수다."""
        samples = generator.generate_many(count=5)
        for s in samples:
            assert 0 <= s.stock <= 999, f"stock={s.stock} 범위 오류"

    def test_sample_no_duplicate_id(self, generator):
        """generate_many(10)으로 생성된 id 10개가 모두 유일하다."""
        samples = generator.generate_many(count=10)
        ids = [s.id for s in samples]
        assert len(ids) == len(set(ids)), f"중복 id 발견: {ids}"

    def test_sample_count(self, generator):
        """generate_many(n)은 정확히 n개를 반환한다."""
        for n in [1, 5, 10]:
            samples = generator.generate_many(count=n)
            assert len(samples) == n, f"요청 {n}개이나 실제 {len(samples)}개"
