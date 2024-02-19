# carbon-intensity-cpu
A little script that sets your cpu scaling governor according to the carbon intensity of your current grid.

The idea is simple, if the grid is currently full of bad carbon intense electricity we want to use less of it. If the grid is green we can use a little more. While there are a lot of problems with this in general this is a good first step.

So why don't our computers scale dynamically according to the grid? Now you can achieve this with a very simple demon that runs in the background and sets your CPU into the state according to the grid.

There is an easy to use `install.sh` script you can use to set everything up for you.

We use electricitymaps.com for the grid intensity.

You will need a token for electricitymaps.com which you can get from https://api-portal.electricitymaps.com/

We get the location of your machine through ipinfo.io . If you don't want this to happen you can set your lat and lng in the config file. For most locations the country is accurate enough. But hopefully we will get better data soon.

