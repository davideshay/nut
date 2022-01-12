#!/bin/sh
kubectl drain ${UPSMON_NODE} --ignore-daemonsets --delete-emptydir-data
/sbin/halt
