
# LXD Alpine Linux image builder

This script provides a way to create [Alpine Linux](http://alpinelinux.org/)
images for their use with [LXD](https://linuxcontainers.org/lxd/).
It's based off the LXC templates.

The image will be built just by installing the `alpine-base` meta-package.
Networking and syslog are enabled by default.


## Usage

In order to build the latest Alpine image just run the script (must be done
as root):

    sudo ./build-alpine

For more options check the help:

    sudo ./build-alpine -h

After the image is built it can be added as an image to LXD as follows:

    lxc image import alpine-v3.3-x86_64-20160114_2308.tar.gz --alias alpine-v3.3


## License

This script uses the same license as the script it was derived from: LGPL 2.1

