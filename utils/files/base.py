# -*- coding = utf-8 -*-
# @time:2024/7/29 10:15
# Author:david yuan
# @File:base_model.py
# @Software:VeSync

from typing import List, Optional, Any

from pydantic import BaseModel


class File(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    columns: Optional[List[str]] = None
    data_path: Optional[str] = None
    type: str = "FILE"

    def get_metadata(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)