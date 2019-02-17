#!/usr/bin/env bash
cd noel-bm3d-executable
if [[ ! -f bm3d.install ]]; then
    wget -O megacmd.zip https://github.com/t3rm1n4l/megacmd/releases/download/0.015/megacmd_0.015_linux_amd64.zip
    unzip megacmd.zip megacmd
    rm megacmd.zip
    chmod +x megacmd
    echo $MEGA_CONFIG > conf.json
    ./megacmd --conf conf.json get mega:/bm3d.install
	rm megacmd conf.json
fi