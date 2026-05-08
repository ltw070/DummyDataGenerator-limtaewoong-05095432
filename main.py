"""main.py - DummyDataGenerator CLI 진입점"""
from __future__ import annotations
import argparse
from pathlib import Path

from app.repository.sample_repository import SampleRepository
from app.repository.order_repository import OrderRepository
from app.generator.seeder import Seeder

DATA_DIR = Path(__file__).parent / "data"
SAMPLE_FILE = DATA_DIR / "samples.json"
ORDER_FILE = DATA_DIR / "orders.json"


def build_seeder() -> Seeder:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return Seeder(
        sample_repo=SampleRepository(file_path=SAMPLE_FILE),
        order_repo=OrderRepository(file_path=ORDER_FILE),
    )


def cmd_seed(args: argparse.Namespace) -> None:
    seeder = build_seeder()
    result = seeder.seed(sample_count=args.samples, order_count=args.orders)
    print(f"Seeded {result.samples_created} samples and {result.orders_created} orders.")


def cmd_clear(args: argparse.Namespace) -> None:
    seeder = build_seeder()
    seeder.clear()
    print("All data cleared.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DummyDataGenerator - 반도체 시료 생산주문관리 시스템 Dummy 데이터 생성 도구"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    seed_parser = subparsers.add_parser("seed", help="Dummy 데이터 생성 후 저장소에 삽입")
    seed_parser.add_argument("--samples", type=int, default=5, help="생성할 Sample 수 (기본값: 5)")
    seed_parser.add_argument("--orders", type=int, default=20, help="생성할 Order 수 (기본값: 20)")
    seed_parser.set_defaults(func=cmd_seed)

    clear_parser = subparsers.add_parser("clear", help="저장소 전체 데이터 삭제")
    clear_parser.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
