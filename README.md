Linux Vendor Firmware Service mirror container

```
mkdir mirror
docker buildx build . -t lvfs_sync
docker run -ti --rm -v $PWD/mirror:/mirror:z lvfs_sync
```



To enable your host to use the mirror
```
# cat /etc/fwupd/remotes.d/remote.conf
[fwupd Remote]
Enabled=true
Type=download
MetadataURI=http://<url>/firmware.xml.gz
FirmwareBaseURI=http://<url>/
```