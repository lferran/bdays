from bdays.api import app
from bdays.settings import load_settings
from bdays.settings import Settings
import uvicorn
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bdays api server")
    parser.add_argument("--config", "-c", default="config.json", required=False)
    args = parser.parse_args()

    settings: Settings = load_settings(args.config)
    uvicorn.run(app, host="0.0.0.0", port=settings.port, log_level="info")
