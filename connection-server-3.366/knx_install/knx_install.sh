apt update && apt-get install -y wget build-essential 

#PTHSEM
tar -zxvf pthsem_2.0.8.tar.gz 
cd pthsem-2.0.8 
./configure 
make && make install && ldconfig

cd ..

# BCUSDK
tar xzvf bcusdk_0.0.5.tar.gz 
cd bcusdk-0.0.5 
./configure \
    --enable-onlyeibd \
    --enable-tpuarts \
    --enable-tpuart \
    --enable-ft12 \
    --enable-eibnetip \
    --enable-eibnetiptunnel \
    --enable-eibnetipserver \
    --enable-groupcache \
    --enable-static=yes \
    --with-pth=yes
make && make install
