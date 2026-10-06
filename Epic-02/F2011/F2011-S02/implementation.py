"""F2011: local Prototype entrypoint; real adapters and approvals pending."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"runtime"))
from core import ConversationSession, Rejected
__all__=["ConversationSession","Rejected"]
