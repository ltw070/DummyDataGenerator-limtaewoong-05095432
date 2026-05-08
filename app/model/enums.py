"""OrderStatus Enum 정의"""
from enum import Enum


class OrderStatus(Enum):
    """주문 상태 흐름: RESERVED → PRODUCING → CONFIRMED → RELEASE / REJECTED"""
    RESERVED = "RESERVED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"
    REJECTED = "REJECTED"
