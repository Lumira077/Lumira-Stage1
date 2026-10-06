"""F2212: local Prototype entrypoint; real adapters and approvals pending."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"runtime"))
from core import Recovery, Rejected
__all__=["Recovery","Rejected"]
