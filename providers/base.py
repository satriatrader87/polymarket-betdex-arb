# providers/base.py
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def get_price(self, market_id):
        pass
