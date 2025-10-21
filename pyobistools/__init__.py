__version__ = "1.0.0"

# Configure pandas for future-compatible behavior
try:
    import pandas as pd
    # Opt-in to pandas 2+ behavior for explicit type handling
    pd.set_option('future.no_silent_downcasting', True)
except (ImportError, ValueError):
    # pandas not installed or option not available in this version
    pass
