"""terminus fastapi backend."""

import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import simulate, fmt_iec, sci

app = FastAPI(title="Terminus API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulateRequest(BaseModel):
    branching: int = Field(default=16, ge=2, le=1000)
    level: int = Field(default=50, ge=1, le=200)
    payload: int = Field(default=43, ge=1, le=10000)
    payload_type: Optional[str] = "zeros"

class LevelData(BaseModel):
    depth: int
    zip_size: float
    zip_size_human: str
    files: int
    files_sci: str
    uncompressed: int
    ratio: float
    ratio_sci: str

class SimulateResponse(BaseModel):
    config: dict
    results: dict
    levels: list[LevelData]

@app.get("/")
def root():
    return {"message": "Terminus API", "docs": "/docs"}

@app.post("/api/simulate", response_model=SimulateResponse)
def api_simulate(req: SimulateRequest):
    r = simulate(req.branching, req.level, req.payload, req.payload_type)
    
    return SimulateResponse(
        config={
            'branching': r['branching'],
            'level': r['level'],
            'payload': r['payload'],
            'payload_type': r['payload_type'],
        },
        results={
            'total_files': r['total_files'],
            'total_files_sci': sci(r['total_files']),
            'total_files_digits': int(math.log10(r['total_files'])) + 1,
            'total_bytes': r['total_bytes'],
            'zip_size': r['zip_size'],
            'zip_size_human': fmt_iec(r['zip_size']),
            'ratio': r['ratio'],
            'ratio_sci': sci(r['ratio']),
        },
        levels=[
            LevelData(
                depth=l['depth'],
                zip_size=l['zip_size'],
                zip_size_human=fmt_iec(l['zip_size']),
                files=l['files'],
                files_sci=sci(l['files']),
                uncompressed=l['uncompressed'],
                ratio=l['ratio'],
                ratio_sci=sci(l['ratio']),
            )
            for l in r['levels']
        ],
    )

@app.get("/api/presets")
def presets():
    return {
        "terminus": {"branching": 16, "level": 50, "payload": 43, "payload_type": "zeros"},
        "small": {"branching": 4, "level": 10, "payload": 100, "payload_type": "text"},
        "medium": {"branching": 8, "level": 25, "payload": 256, "payload_type": "zeros"},
        "extreme": {"branching": 32, "level": 100, "payload": 1024, "payload_type": "random"},
    }
