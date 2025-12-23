# <img src="images/logo.png" width="50" height="50"> Auto Utility Meter
# Auto Utility Meter

Auto Utility Meter is a Home Assistant integration that simplifies energy monitoring. It automatically converts Power (W) into Energy (kWh) using the Riemann Sum and creates utility meters for your chosen intervals.

## Features
* **Automatic Conversion:** Converts Watt values to kWh.
* **Selected Intervals:** Automatically creates sensors for intervals like daily, monthly, or yearly.
* **Energy Dashboard Ready:** Sensors are pre-configured for the official HA Energy Dashboard.

## Installation

### Via HACS (Recommended)
1. Go to **HACS** > **Integrations**.
2. Click the three dots in the top right and select **Custom repositories**.
3. Paste the link to this GitHub repository.
4. Select **Integration** as the category and click **Add**.
5. Click **Download** on the new "Auto Utility Meter" card.
6. **Restart** Home Assistant.

### Manual
1. Copy the `auto_utility_meter` folder from `custom_components` to your `config/custom_components/` directory.
2. **Restart** Home Assistant.

## Setup
1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Auto Utility Meter** and follow the configuration steps.

---
*Created for the Home Assistant Community.*
