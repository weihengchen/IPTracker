USER=[name]
WEB=[website]

su 
crontab -l >> .mycron_tmp
echo "*/5 * * * * curl http://$WEB/record?name=$USER"
crontab .mycron_tmp
rm .mycron_tmp
