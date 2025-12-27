from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Orchid Disease Detector"
    api_version: str = "v1"
    debug: bool = False

    # Database settings (if applicable)
    database_url: str = "sqlite:///./test.db"

    # Model settings
    model_path: str = "./models/trained_model.h5"

    #image path
    image_path: str = "../images/"

    class Config:
        env_file = ".env"

settings = Settings()