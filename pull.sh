#!/usr/bin/expect -f
spawn ./update.sh
expect "Username for 'http://gitlab.9tong.com'"
send -- "lihaitao\n"
expect "Password for 'http://lihaitao@gitlab.9tong.com'"
send -- "qq2958635\n"
interact
