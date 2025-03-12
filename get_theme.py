import os
import toml

def get_theme_colors():
    # Define the expected config path; adjust if needed.
    config_path = os.path.join(".streamlit", "config.toml")
    try:
        with open(config_path, "r") as f:
            config = toml.load(f)
        theme = config.get("theme", {})
        primary_color = theme.get("primaryColor", "#de001f")
        secondary_bg = theme.get("secondaryBackgroundColor", "#e9e9e9")
        text_color = theme.get("textColor", "#201922")
        return {"primary": primary_color, "secondary_bg": secondary_bg, "text": text_color}
    except Exception as e:
        # Fallback values if config isn't found or parsing fails.
        return {"primary": "#de001f", "secondary_bg": "#e9e9e9", "text": "#201922"}

# Usage example:
theme_colors = get_theme_colors()
