# Visuales UCLV Explorer - Refactored

This is a deep refactor of the Visuales UCLV Desktop application, applying Clean Architecture principles and modern Python libraries.

## Architecture Overview

The project follows a modular structure:
- **visuales_uclv/core**: Configuration (Settings) and Logging.
- **visuales_uclv/domain**: Business logic, Models (`nodes.py`), and Interfaces. Includes the `SearchEngine`.
- **visuales_uclv/data**: Implementation of data access.
  - `clients`: Network clients (Scraper, Downloader).
  - `repositories`: Local data management (Tree structure caching).
- **visuales_uclv/presentation**: PySide6-based UI components.

## How to Run

1. Install dependencies:
   ```bash
   pip install PySide6 rapidfuzz aiohttp qt-material pydantic-settings beautifulsoup4 treelib lxml
   ```
2. Run the application:
   ```bash
   python -m visuales_uclv.presentation.main_window
   ```

## How to Build

### Windows
```bash
pyinstaller --name "VisualesUCLV" --onefile --windowed --icon=icon.ico visuales_uclv/presentation/main_window.py
```

### Linux
```bash
pyinstaller --name "VisualesUCLV" --onefile --windowed visuales_uclv/presentation/main_window.py
```

## Migration Notes

1. **PyQt5 to PySide6**: Migrated to the modern, officially supported Qt for Python.
2. **Modern UI**: Added `qt-material` for a consistent, professional dark theme.
3. **Async Core**: Network requests and downloads now use `aiohttp` and `asyncio`, preventing UI freezes without complex manual threading.
4. **Clean Architecture**: Decoupled scraping logic from UI. The `SearchEngine` and `Downloader` are now independent modules.
5. **Fuzzy Search**: Replaced basic substring matching with `RapidFuzz` for ranked, fault-tolerant search results.
6. **Improved Downloader**: New implementation supports resuming partially downloaded files and handles multiple concurrent tasks efficiently.
