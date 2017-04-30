Installation:
sudo pip install Flask
sudo pip install flask_wtf

Usage: python run.py

Open the webpage at http://localhost:5000

nohup python run.py > /dev/null 2>&1 &
sudo ss -lptn 'sport = :5000'

	State      Recv-Q Send-Q        Local Address:Port          Peer Address:Port 
	LISTEN     0      128                       *:5000                     *:*      
	users:(("python",24282,3)) # pid = 24282

sudo kill -9 <pid> 