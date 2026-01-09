<p align="center">
  <img src="https://raw.githubusercontent.com/yunusp01/auto_utility_meter/main/images/logo.png" width="400" alt="Auto Utility Meter Logo">
</p>

![Version](https://img.shields.io/github/v/release/yunusp01/auto_utility_meter?style=for-the-badge)
![License](https://img.shields.io/github/license/yunusp01/auto_utility_meter?style=for-the-badge)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

**Auto Utility Meter** is a powerful Home Assistant integration designed to automate your resource tracking. It eliminates the manual effort of setting up Riemann Sum sensors and Utility Meters, providing a seamless experience for monitoring your home's consumption.

---

## ✨ Features
* **⚡ Automatic Energy Conversion:** Instantly converts Power (W) into Energy (kWh) using the Riemann Sum integration.
* **💧 Water & Gas Support:** Now supports tracking for Water (m³) and Gas (m³) flow sensors.
* **📅 Flexible Intervals:** Automatically generates sensors for Daily, Weekly, Monthly, Quarterly, or Yearly tracking.
* **📊 Energy Dashboard Ready:** All sensors are pre-configured with the correct `device_class` and `state_class` to work instantly with the official HA Energy Dashboard.
* **🛠️ UI-Based Configuration:** Fully manageable through the Home Assistant Integrations menu—no YAML required!

## 🚀 Installation

### Via HACS (Recommended)
1. Go to **HACS** > **Integrations**.
2. Click the three dots in the top right and select **Custom repositories**.
3. Paste the link: `https://github.com/yunusp01/auto_utility_meter`.
4. Select **Integration** and click **Add**.
5. Click **Download** on the new card and **Restart** Home Assistant.

## ⚙️ Setup
1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Auto Utility Meter**.
4. Follow the setup dialog to select your source sensor and desired intervals.

---
<p align="center"><i>Created with ❤️ for the Home Assistant Community.</i></p>
