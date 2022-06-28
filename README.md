# Linux Vendor Firmware Service mirror container
Build and run mirror

```sh
mkdir mirror
docker buildx build . -t lvfs_sync
docker run -ti --rm -v $PWD/mirror:/mirror:z lvfs_sync
```


---

## To host the mirror

```sh
docker buildx build . -t nginx
docker run -ti --rm -v $PWD/mirror:/mirror:z nginx
```
---

## To enable your host to use the mirror
```sh
# cat /etc/fwupd/remotes.d/remote.conf
[fwupd Remote]
Enabled=true
Type=download
MetadataURI=http://<url>/firmware.xml.gz
FirmwareBaseURI=http://<url>/
```