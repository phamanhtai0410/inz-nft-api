FROM 968557029040.dkr.ecr.ap-southeast-1.amazonaws.com/esollabs/cicd:sh-python-ba4ec63-dirty


COPY requirements.txt /
COPY lib/requirements.txt /lib/requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r /lib/requirements.txt
RUN pip install -r requirements.txt
RUN pip install "Flask[async]"

COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps
WORKDIR /webapps