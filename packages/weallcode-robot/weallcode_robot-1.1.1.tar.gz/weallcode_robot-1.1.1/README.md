# We All Code Robot

[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> This README is for developing the underlying server (lua) code for a robot.
To install the Python client (e.g. to control a robot over wifi), refer to the
[Client README](./weallcode_robot/README.md).

## Table of Contents

- [Requirements](#requirements)
- [Install](#install)
- [Setup](#setup)
- [API](#api)
- [Diagram](#diagram)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python >= 3.7
- Pip >= 10.0
- [VCP Drivers][vcp-drivers] (MacOS)

## Install

```bash
make install
```

If you're using MacOS, you'll need to manually install the
[VCP Drivers][vcp-drivers] in order to recognize USB serial devices.

### Flash Firmware

After flashing the firmware, restart the board and wait for the filesystem to be
formatted. When complete, you can hit `ctrl-]`.

```bash
make flash
```

When complete, you should see a message saying "lua: cannot open init.lua" (this is because there is firmware but no software).

*Common Issues:*
- Sometimes you'll need to hit enter to see the prompt.
- Sometimes on Linux you need to unplug and replug the usb cable after flashing.

Last firmware built on the [Cloud Builder](https://nodemcu-build.com/) was:

Modules: `apa102,bit,crypto,file,gpio,mdns,net,node,pwm,tmr,wifi`

LFS size: 64KB

### Upload Software

```bash
make upload <robotname>
```

### Start a terminal to view logs

```bash
make terminal
```

When complete, you can hit `ctrl-]`.

## Setup

For the first two minutes that the robot is turned on, an open WiFi network
named `We All Code [<robotname>]` will be broadcast. Join the network to be
brought to a captive portal setup page. On this page you can instruct the robot
which WiFi network it should join on boot. These settings will be saved until
changed manually.

## API

Once attached to a network, the robot will listen for HTTP requests at
`http://<robotname>.local` with the following endpoints:

| Endpoint   | Description                                              |
| :--------- | :------------------------------------------------------- |
| `/`        | Shows the WiFi Setup page                                |
| `/hello`   | Returns a minimal hello response                         |
| `/command` | Accepts commands for the robot's wheels, LED, and buzzer |
| `/gamepad` | Displays a controller compatible with several Gamepads   |
| `/update`  | Triggers a code update                                   |
| `/wifi`    | WiFi Setup submission page                               |

### Endpoint: `/command`

> Note: this endpoint can be upgraded to a websocket and will accept commands in the
form of a search string.

| Param  | Type  | Values                  | Example            |
| :----- | :---- | :---------------------- | :----------------- |
| left   | int   | -100 to 100             | left=87            |
| right  | int   | -100 to 100             | right=93           |
| led    | mixed | `r,g,b` or `off`        | led=255,0,34       |
| buzzer | mixed | `hz,period` or `off`    | buzzer=1000,1023   |


*Examples:*

```
http://robotname.local/command?left=100&right=100&led=255,255,255&buzzer=1000,1023
```

```
ws://robotname.local/command

data: ?left=100&right=100&led=255,255,255&buzzer=1000,1023
data: ?left=0&right=0&led=off&buzzer=off
```

### Endpoint: `/update`

> Note: downloading the `.img` file from an https source is not yet supported as
the SSL connection requires too much memory.

| Param  | Type   | Description  | Default                    |
| :----- | :----- | :----------- | :------------------------- |
| host   | string | Domain name  | `robots.weallcode.org`     |
| dir    | string | Path to file | `/lfs`                     |
| image  | string | File name    | `flash.img`                |

*Examples:*

```
http://robotname.local/update
```

```
http://robotname.local/update?host=wac.fyi&dir=/&image=flash.img
```

### Endpoint: `/wifi`

Note: Only WiFi WPA2 networks are currently supported.

| Param  | Type   | Description           |
| :----- | :----- | :-------------------- |
| ssid   | string | WiFi network name     |
| padd   | string | WiFi network password |

*Examples:*

```
http://robotname.local/wifi?ssid=We+All+WiFi&pass=Coder4life
```

## Diagram

![fritzing](./assets/fritzing/fritzing.svg)

## Maintainers

[@danielmconrad](https://github.com/danielmconrad)

## Contributing

PRs accepted.

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

MIT © 2019 We All Code

[vcp-drivers]: https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers
