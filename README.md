Running with docker:  
create build:  
  sudo docker build -t teleg_bot:latest .  
run build  
  sudo docker run -d -e TOKEN="your_token" teleg_bot:latest
