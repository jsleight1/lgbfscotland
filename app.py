from lgbfscotland.lgbfscotland import lgbfscotland
from pathlib import Path

www_dir = Path(__file__).parent / "www"
app = lgbfscotland(static_assets=www_dir)
