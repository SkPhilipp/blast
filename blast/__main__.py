import fire

from blast.main import CLI


def main():
    fire.Fire(component=CLI, name="blast")
