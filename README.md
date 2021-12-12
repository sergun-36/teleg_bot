Running with docker:
create build:
sudo docker build -t teleg_bot:teleg_bot .
run build
sudo docker run -d -p 5000:5000 teleg_bot:teleg_bot