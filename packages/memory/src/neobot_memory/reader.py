"""MemoryReader Protocol — 记忆读取抽象"""

from __future__ import annotations

from typing import Protocol


class MemoryReader(Protocol):
    """记忆读取接口，MemoryService 结构性满足此接口"""

    async def recall(
        self, conversation_id: str, query: str, limit: int = 5
    ) -> list[str]: ...
