# Plex Audio and Subtitle Stream Setter

This Python script allows you to interactively set default **audio** and **subtitle** streams for each episode of a TV series in your Plex library. It's useful for bulk updates across seasons, especially when stream defaults need to be corrected or standardized.

## Features

- Select a Plex library section (e.g., *Series*)
- Choose a specific TV series
- For each season:
  - Optionally skip processing
  - View and select from available audio and subtitle stream configurations
  - Apply chosen streams as defaults for episodes with matching stream sets

## Requirements

- Python 3.6+
- Plex Media Server
- Plex API Token

## Installation

1. Clone or download this script.
2. Install required Python packages:

```
pip install -r requirements.txt
```

3. Create a file named `.env` in the same directory as the script, and add the following lines:

```
PLEX_URL=http://your-plex-server:32400
TOKEN=your_plex_token
```

> 💡 **How to find your Plex token**:  
> - Open the Plex web interface.  
> - Press F12 to open Developer Tools.  
> - Go to the **Network** tab.  
> - Refresh the page.  
> - Look for a request URL containing `X-Plex-Token`, and copy its value.

## Usage

Run the script using:

```
./plex_set_streams.py
```

### You will be prompted to:

1. Select the Plex library section  
2. Enter the name of the TV series  
3. For each season:
   - Choose whether to skip it
   - Select a default **subtitle** stream
   - Select a default **audio** stream

## Notes

- The script only modifies metadata on your Plex server.
- Media files are not changed.
- You can rerun the script any time to update stream selections.

## Disclaimer

Use at your own risk. This script makes changes to your Plex server via its API.

