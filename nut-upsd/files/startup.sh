#!/bin/sh
#
#  Provided to you under the terms of the Simplified BSD License.
#
#  Copyright (c) 2019. Gianpaolo Del Matto, https://github.com/gpdm, <delmatto _ at _ phunsites _ dot _ net>
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

nutCfgVolume="/etc/nut"
nutCfgFiles="ups.conf upsd.conf upsd.users"

echo "*** NUT upsd startup ***"

# more sanity: make sure our config files stick around

# sleep 600

# initialize UPS driver
printf "Starting up the UPS drivers ...\n"
/usr/sbin/upsdrvctl start || { printf "ERROR on driver startup.\n"; exit; }

# run the ups daemon
printf "Starting up the UPS daemon ...\n"
exec /usr/sbin/upsd -D -u root || { printf "ERROR on daemon startup.\n"; exit; }
