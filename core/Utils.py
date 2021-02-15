from pathlib import Path

def rootDir() -> str:
	return str(Path(__file__).resolve().parent.parent)
