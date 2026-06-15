from app.core.config import Settings


def test_parse_cors_origins_from_comma_separated_string() -> None:
    assert Settings.parse_cors_origins(
        "http://localhost:3000, http://127.0.0.1:3000"
    ) == ["http://localhost:3000", "http://127.0.0.1:3000"]


def test_parse_cors_origins_filters_empty_entries() -> None:
    origins = Settings.parse_cors_origins(
        "http://localhost:3000,,http://127.0.0.1:3000",
    )
    assert origins == [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


def test_parse_cors_origins_accepts_list() -> None:
    origins = ["http://localhost:3000"]
    assert Settings.parse_cors_origins(origins) == origins


def test_settings_ignores_unknown_env_vars(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setenv("MEMORI_API_KEY", "memori-test")
    monkeypatch.setenv("UNRELATED_SETTING", "ignored")

    settings = Settings(_env_file=None)

    assert settings.openai_api_key == "openai-test"
    assert settings.memori_api_key == "memori-test"
    assert settings.openai_model == "gpt-4o-mini"


def test_settings_loads_cors_origins_from_env(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setenv("MEMORI_API_KEY", "memori-test")
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )

    settings = Settings(_env_file=None)

    assert settings.cors_origins == [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
