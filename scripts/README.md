# History commands to install a new server

ssh -i ~/.ssh/key user@your-server

sudo useradd paws
sudo groupadd paws
sudo passwd paws
sudo cp -R /root/.ssh /home/paws
sudo chown -R paws:paws /home/paws
sudo chmod -R 755 /home/paws/.ssh
sudo usermod -a -G wheel paws
sudo usermod -a -G nginx paws

cd /home/paws
git clone https://github.com/rhpit/paws-imgsrv.git
cd /home/paws/paws-imgsrv
sudo pip install -r requirements.txt --upgrade

sudo mkdir -p /var/www/html/imgsrv
cd /home/paws/paws-imgsrv/imgsrv
sudo cp -R -v * /var/www/html/imgsrv/

cd /home/paws/paws-imgsrv/scripts
sudo cp nginx/nginx.conf /etc/nginx.conf
sudo cp nginx/imgsrv.my-domain.com.conf /etc/nginx/conf.d/
sudo cp systemctl/imgsrv.service /etc/systemd/system/imgsrv.service

sudo chown -R paws:nginx /var/www/html/imgsrv

* Selinux set context mng or disable it if you are not familiar (/etc/selinux/config)

sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --reload

sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx

sudo systemctl start imgsrv
sudo systemctl enable imgsrv
sudo systemctl status imgsrv


## maintenance or web-server restart

ssh -i ~/.ssh/key user@your-server

sudo systemctl restart nginx
sudo systemctl status nginx

sudo systemctl restart imgsrv
sudo systemctl status imgsrv

check logs for troubleshooting:

access_log  /var/log/nginx/imgsrv-http-access.log
error_log   /var/log/nginx/imgsrv-http-error.log


## deploy new releases or code update

ssh -i ~/.ssh/key user@your-server

cd /home/paws/paws-imgsrv
git fetch --all
git pull
cd /home/paws/paws-imgsrv/imgsrv
sudo cp -R -v * /var/www/html/imgsrv/

sudo systemctl restart imgsrv
sudo systemctl status imgsrv


## imgsrv nginx logs

access_log  /var/log/nginx/imgsrv-http-access.log
error_log   /var/log/nginx/imgsrv-http-error.log


## troubleshooting

ps aux |grep nginx
ps aux |grep imgsrv

check logs:
	access_log  /var/log/nginx/imgsrv-http-access.log
	error_log   /var/log/nginx/imgsrv-http-error.log

check selinux
check firewalld
check paws user: $ id paws
