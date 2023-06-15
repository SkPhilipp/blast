import fire
from blast.main import CLI
import sys

if __name__ == "__main__":
    fire.Fire(component=CLI, name="blast")
