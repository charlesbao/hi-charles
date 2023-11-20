+++
date = "2022-06-02"
tags = ["nginx","linux","node","优化"]
title = "Nginx 反向代理缓存配置"
+++

> 缓存Nginx服务器中的文件,便于缓存以减轻服务器的压力<!--more-->

**我的nginx服务配置文件**  
/etc/nginx/nginx.conf
```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections  1024;
}


http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    large_client_header_buffers 4 64k;
    client_max_body_size 8m;
    client_body_buffer_size 128k;

    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 64k;
    fastcgi_buffers 4 64k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;

    gzip on;
    gzip_min_length 1k;
    gzip_buffers 4 16k;
    gzip_http_version 1.1;
    gzip_comp_level 2;
    gzip_types text/plain application/x-javascript text/css application/xml;
    gzip_vary on;

    proxy_connect_timeout 300;
    proxy_send_timeout 300;
    proxy_read_timeout 300;
    proxy_buffer_size 64k;
    proxy_buffers 4 512k;
    proxy_busy_buffers_size 512k;
    proxy_temp_file_write_size 512k;
    proxy_buffering on;
    proxy_cache_valid any 1d;
    proxy_cache_path /etc/nginx/proxy-cache levels=1:2 keys_zone=my-cache:8m max_size=1000m inactive=600m;
    proxy_temp_path /etc/nginx/proxy-temp;

    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-NginX-Proxy true;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    
    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;
}

```

/etc/nginx/conf.d/default.conf  
```
server {
   listen 80;
   server_name charlesbao.com www.charlesbao.com;
   location / {

      proxy_pass http://localhost:2368/;

      proxy_cache my-cache;
      proxy_cache_valid 200;
      proxy_cache_key $host$uri$is_args$args;

      client_max_body_size 10m;
      client_body_buffer_size 128k;
      proxy_connect_timeout 90;
      proxy_send_timeout 90;
      proxy_read_timeout 90;
      proxy_buffer_size 4k;
      proxy_buffers 4 32k;
      proxy_busy_buffers_size 64k;
      proxy_temp_file_write_size 64k;
   }

   location /NginxStatus {
      stub_status on;
      access_log on;
      auth_basic "NginxStatus";
   }
}
```
