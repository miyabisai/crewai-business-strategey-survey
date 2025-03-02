from crewai import Tool
from typing import Any, Dict, Optional

class CustomTool(Tool):
    def __init__(
        self,
        name: str,
        description: str,
        func: Any,
        parameters: Optional[Dict] = None
    ):
        super().__init__(
            name=name,
            description=description,
            func=func,
            parameters=parameters
        )

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)