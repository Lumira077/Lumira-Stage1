"""Development entrypoint, no actual model/hardware inference."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"runtime"))
from core import TTSPlanner, Context, Rejected
