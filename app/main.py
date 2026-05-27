from app.core.application import create_app

app = create_app()


def start() -> None:
    from app.entrypoint import main

    main()
