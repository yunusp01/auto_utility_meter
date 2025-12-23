<p align="center">
  <img src="https://raw.githubusercontent.com/yunusp01/auto_utility_meter/main/images/logo.png" width="150" height="150" alt="Auto Utility Meter Logo">
</p>

<h1 align="center">Auto Utility Meter</h1>

<p align="center">
  <strong>Auto Utility Meter</strong> is a Home Assistant integration that simplifies energy monitoring. It automatically converts Power (W) into Energy (kWh) using the Riemann Sum and creates utility meters for your chosen intervals.
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/yunusp01/auto_utility_meter?style=flat-square" alt="Current Version">
  <img src="https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square" alt="HACS Custom">
  <img src="https://img.shields.io/github/license/yunusp01/auto_utility_meter?style=flat-square" alt="License">
</p>

---

## Features
* **Automatic Conversion:** Converts Watt values to kWh.
* **Selected Intervals:** Automatically creates sensors for intervals like daily, monthly, or yearly.
* **Energy Dashboard Ready:** Sensors are pre-configured for the official HA Energy Dashboard.

## Installation

### Via HACS (Recommended)
1. Go to **HACS** > **Integrations**.
2. Click the three dots in the top right and select **Custom repositories**.
3. Paste the link to this GitHub repository: `https://github.com/yunusp01/auto_utility_meter`
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
<p align="center">
  <i>Created for the Home Assistant Community.</i>
</p>
