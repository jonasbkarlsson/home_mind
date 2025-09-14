# Home Mind

[![GitHub Release][releases-shield]][releases]
[![Codecov][coverage-shield]][coverage]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

![Icon](assets/logo.png)

The Home Mind integration ...

## Requirements
- Home Assistant version 2024.12 or newer.
- Frigate integraton
- Assist Satellite

## Features
- ...

## Installation

### HACS
1. In Home Assistant go to HACS and search for "". Click on "Home Mind" and then on "Download".

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jonasbkarlsson&repository=home_mind&category=integration)

2. In Home Assistant go to Settings -> Devices & Services -> Integrations. Click on "+ Add integration" and search for "".

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=home_mind)

### Manual

1. Using the tool of choice open the folder for your Home Assistant configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` folder there, you need to create it.
3. In the `custom_components` folder create a new folder called `home_mind`.
4. Download _all_ the files from the `custom_components/home_mind/` folder in this repository.
5. Place the files you downloaded in the new folder you created.
6. Restart Home Assistant.
7. In Home Assistant go to Settings -> Devices & Services -> Integrations. Click on "+ Add integration" and search for "".

## Configuration

The configuration is done in the Home Assistant user interface.

...

With the exception of Name, the above configuration items can be changed after intial configuration in Settings -> Devices & Services -> Integrations ->  -> 1 device -> Configure. To change Name, the native way to rename Integrations or Devices in Home Assistant can be used.

[home_mind]: https://github.com/jonasbkarlsson/home_mind
[releases-shield]: https://img.shields.io/github/v/release/jonasbkarlsson/home_mind?style=for-the-badge
[releases]: https://github.com/jonasbkarlsson/home_mind/releases
[coverage-shield]: https://img.shields.io/codecov/c/gh/jonasbkarlsson/home_mind?style=for-the-badge&logo=codecov
[coverage]: https://app.codecov.io/gh/jonasbkarlsson/home_mind
[license-shield]: https://img.shields.io/github/license/jonasbkarlsson/home_mind?style=for-the-badge
[license]: https://github.com/jonasbkarlsson/home_mind/blob/main/LICENSE
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Jonas%20Karlsson%20@jonasbkarlsson-41BDF5.svg?style=for-the-badge
[user_profile]: https://github.com/jonasbkarlsson
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-FFDD00.svg?style=for-the-badge&logo=buymeacoffee
[buymecoffee]: https://www.buymeacoffee.com/jonasbkarlsson
