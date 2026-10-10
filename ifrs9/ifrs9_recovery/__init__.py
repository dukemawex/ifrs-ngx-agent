"""Auditable recovery and verification pipeline for the Nigerian IFRS 9 bank panel.

Every stage reads the frozen inputs, writes only under data/, outputs/, state/,
cache/, logs/ and reports/, and checkpoints after each unit of work.
"""

__version__ = "0.1.0"
