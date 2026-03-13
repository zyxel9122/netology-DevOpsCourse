Задача 1.

kirillbastrykin@iMac-Kirill packer % yc compute image list
+----------------------+--------------------------------------+-------------------+----------------------+--------+
|          ID          |                 NAME                 |      FAMILY       |     PRODUCT IDS      | STATUS |
+----------------------+--------------------------------------+-------------------+----------------------+--------+
| fd8m99pg82tt5595q2di | debian-12-nginx-2026-03-12t12-59-12z | debian-web-server | f2ed8nhicub2u3dv9tpd | READY  |
+----------------------+--------------------------------------+-------------------+----------------------+--------+

Задача 2.

kirillbastrykin@iMac-Kirill VMbox % vagrant ssh
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-189-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri 13 Mar 2026 05:33:50 AM UTC

  System load:           0.36
  Usage of /:            13.8% of 30.34GB
  Memory usage:          25%
  Swap usage:            0%
  Processes:             153
  Users logged in:       0
  IPv4 address for eth0: 10.0.2.15
  IPv6 address for eth0: fd17:625c:f037:2:a00:27ff:fecb:1a1d


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento

Use of this system is acceptance of the OS vendor EULA and License Agreements.
vagrant@server1:~$ 

vagrant@server1:~$ docker version && docker compose version
Client: Docker Engine - Community
 Version:           28.1.1
 API version:       1.49
 Go version:        go1.23.8
 Git commit:        4eba377
 Built:             Fri Apr 18 09:52:18 2025
 OS/Arch:           linux/amd64
 Context:           default
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.49/version": 
dial unix /var/run/docker.sock: connect: permission denied
vagrant@server1:~$ 

Задача3. 

==> yandex: Waiting for image to complete...
==> yandex: Success image create...
==> yandex: Destroying boot disk...
==> yandex: Disk has been deleted!
Build 'yandex' finished after 2 minutes 38 seconds.

==> Wait completed after 2 minutes 38 seconds

==> Builds finished. The artifacts of successful builds are:
--> yandex: A disk image was created: debian-12-docker (id: fd8d51rvg2pllhe0db9f) with family name 

zyxel9122@compute-vm-2-2-20-hdd-1773384917851:~$ yxel9122@compute-vm-2-2-20-hdd-1773384917851:~$ docker version
Client: Docker Engine - Community
 Version:           29.3.0
 API version:       1.54
 Go version:        go1.25.7
 Git commit:        5927d80
 Built:             Thu Mar  5 14:25:43 2026
 OS/Arch:           linux/amd64
 Context:           default
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
zyxel9122@compute-vm-2-2-20-hdd-1773384917851:~$ 

zyxel9122@compute-vm-2-2-20-hdd-1773384917851:~$ htop --version
htop 3.2.2
zyxel9122@compute-vm-2-2-20-hdd-1773384917851:~$ tmux --version
usage: tmux [-2CDlNuvV] [-c shell-command] [-f file] [-L socket-name]
            [-S socket-path] [-T features] [command [flags]]
zyxel9122@compute-vm-2-2-20-hdd-1773384917851:~$ tmux --help
usage: tmux [-2CDlNuvV] [-c shell-command] [-f file] [-L socket-name]
            [-S socket-path] [-T features] [command [flags]]
