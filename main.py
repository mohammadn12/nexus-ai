import sys
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )


def main():

    try:

        from desktop.app import start_app

        start_app()

    except Exception as error:

        print()
        print("=" * 60)
        print("NEXUS STARTUP ERROR")
        print("=" * 60)
        print(error)
        print("=" * 60)
        print()

        input(
            "Press Enter to close..."
        )


if __name__ == "__main__":

    main()