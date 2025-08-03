"""Main module for watch duty crawler.

This module provides the main entry point for the subtitle fetching system.
"""

from .models import Work


def main() -> None:
    """Main entry point for the application."""
    print("Subtitle fetching system initialized.")
    
    # Example usage (will be implemented when AI service is ready)
    anime_list = [
        Work(title="進撃の巨人", official_url="https://shingeki.tv/"),
        Work(title="呪術廻戦", official_url="https://jujutsukaisen.jp/"),
    ]
    
    print(f"Ready to process {len(anime_list)} anime titles...")
    print("AI service interface ready for implementation.")


if __name__ == "__main__":
    main()
