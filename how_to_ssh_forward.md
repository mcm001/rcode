from chromebook:
sudo ssh -L 100:localhost:8809 server@morley3d.com -p 222

from server:
ssh -L 8809:localhost:80 pi@10.1.10.22
