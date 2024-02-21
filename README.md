# carbon-intensity-cpu
A little script that sets your cpu scaling governor according to the carbon intensity of your current grid.

The idea is simple, if the grid is currently full of bad carbon intense electricity we want to use less of it. If the grid is green we can use a little more. While there are a lot of problems with this in general this is a good first step.

So why don't our computers scale dynamically according to the grid? Now you can achieve this with a very simple demon that runs in the background and sets your CPU into the state according to the grid.

There is an easy to use `install.sh` script you can use to set everything up for you.

We use electricitymaps.com for the grid intensity.

You will need a token for electricitymaps.com which you can get from https://api-portal.electricitymaps.com/

We get the location of your machine through ipinfo.io . If you don't want this to happen you can set your lat and lng in the config file. For most locations the country is accurate enough. But hopefully we will get better data soon.

## Config

Following parameters can be set in a config file (`/etc/eco-cpu.conf`) or as parameters:

- `-c`: The path of the config file
- `--powersave-state`: The name of the state that represents power save. You can find the supported states under /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_governors Please not that if you have multiple cpus some might have different scaling governors available. Please check all cores
- `--performance-state`: The name of the state that represents performance.
- `--lat`: The latitude of where your server is located. This can be an approximation. If this is not supplied we will try and get the location through ipinfo.io.
- `--lng`: The longitude of where your server is located. This can be an approximation. If this is not supplied we will try and get the location through ipinfo.io.
- `-wg`: The carbon intensity value under which you want to consider the power mix to be "green". Defaults to 100 which could be discussed.
- `--token`: The electricitymaps token. This is probably the only one that is really "needed".

## Future features/ taks

- [ ] Integrate logging and RAPL readings so it is clear how often changes really occur and how much is actually saved on average (this can be derived later statistically)
- [ ] To boost the effect activating C8 states.
- [ ] To boost the effect turn off turbo boost.
