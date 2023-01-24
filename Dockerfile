FROM ubuntu:22.04
RUN apt update && apt install -y python3 \
		python3-pip \
		libgtk-3-dev \
		xauth \
		&& pip3 install attrdict3 \
		&& pip3 install matplotlib \
		&& pip3 install requests \
		&& pip3 install psutil \
		&& pip3 install wxPython
ENV DISPLAY=:0