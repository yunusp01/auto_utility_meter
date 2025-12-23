<p align="center">
  <img src="https://raw.githubusercontent.com/yunusp01/auto_utility_meter/main/images/logo.png" width="400" alt="Auto Utility Meter Logo">
</p>

![Version](https://img.shields.io/github/v/release/yunusp01/auto_utility_meter?style=for-the-badge)
![License](https://img.shields.io/github/license/yunusp01/auto_utility_meter?style=for-the-badge)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

**Auto Utility Meter** is a Home Assistant integration that simplifies energy monitoring. It automatically converts Power (W) into Energy (kWh) using the Riemann Sum and creates utility meters for your chosen intervals.

---

## Features
* **Automatic Conversion:** Converts Watt values to kWh.
* **Selected Intervals:** Automatically creates sensors for intervals like daily, monthly, or yearly.
* **Energy Dashboard Ready:** Sensors are pre-configured for the official HA Energy Dashboard.

## Installation

### Via HACS (Recommended)
1. Go to **HACS** > **Integrations**.
2. Click the three dots in the top right and select **Custom repositories**.
3. Paste the link: `https://github.com/yunusp01/auto_utility_meter`
4. Select **Integration** and click **Add**.
5. Click **Download** on the new card and **Restart** Home Assistant.

## Setup
1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Auto Utility Meter**.

---
<p align="center"><i>Created for the Home Assistant Community.</i></p>
