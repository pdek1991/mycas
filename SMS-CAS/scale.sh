
#!/bin/bash


cd /root/mycas/SMS-CAS
rm -f result
tps=$(<tps.txt)
if (( $tps > 0 && $tps < 5 )); then
echo "TPS between 0 to 9" > result
docker service update --replicas 1 mycas_sms-cas

elif (( $tps > 5 && $tps < 10 )); then
echo "Current TPS:- $tps" >> result
docker service update --replicas 4 mycas_sms-cas
fi
elif (( $tps > 10 && $tps < 20 )); then
echo "TPS between 10 to 20" >> result
docker service update --replicas 3 mycas_sms-cas
elif (( $tps > 20 && $tps < 30 )); then
echo "TPS between 20 to 30" >> result
docker service update --replicas 5 mycas_sms-cas
elif (( $tps >= 30 && $tps <= 40 )); then
echo "TPS between 30 to 40" >> result
docker service update --replicas 7 mycas_sms-cas
else
echo "TPS:$tps too high rate Limit transactions" >> result
fi
