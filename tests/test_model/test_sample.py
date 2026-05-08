"""Phase 1 - Red: Sample 도메인 모델 테스트"""
import pytest
from app.model.sample import Sample


class TestSample:
    def test_sample_creation(self):
        """Sample 객체가 올바르게 생성된다."""
        sample = Sample(
            id="S-001",
            name="실리콘 웨이퍼-8인치",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock=100,
        )
        assert sample.id == "S-001"
        assert sample.name == "실리콘 웨이퍼-8인치"
        assert sample.avg_production_time == 0.5
        assert sample.yield_rate == 0.92
        assert sample.stock == 100

    def test_sample_field_types(self):
        """Sample 필드 타입이 올바르다."""
        sample = Sample(
            id="S-002",
            name="GaN 에피택셜-4인치",
            avg_production_time=0.3,
            yield_rate=0.78,
            stock=50,
        )
        assert isinstance(sample.id, str)
        assert isinstance(sample.name, str)
        assert isinstance(sample.avg_production_time, float)
        assert isinstance(sample.yield_rate, float)
        assert isinstance(sample.stock, int)

    def test_sample_to_dict(self):
        """Sample을 dict로 직렬화할 수 있다."""
        sample = Sample(
            id="S-003",
            name="SiC 파워기판-6인치",
            avg_production_time=0.8,
            yield_rate=0.92,
            stock=200,
        )
        data = sample.to_dict()
        assert data["id"] == "S-003"
        assert data["name"] == "SiC 파워기판-6인치"

    def test_sample_from_dict(self):
        """dict에서 Sample을 역직렬화할 수 있다."""
        data = {
            "id": "S-004",
            "name": "포토레지스트-PR7",
            "avg_production_time": 0.2,
            "yield_rate": 0.95,
            "stock": 75,
        }
        sample = Sample.from_dict(data)
        assert sample.id == "S-004"
        assert sample.yield_rate == 0.95
