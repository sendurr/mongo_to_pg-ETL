FROM python:3.5.1
RUN apt-get update && apt-get install \
  && rm -rf /var/lib/apt/lists/*

# Set up python environment
RUN mkdir /gigsterpg
RUN export PYTHONPATH=$PYTHONPATH:/gigsterpg
WORKDIR /gigsterpg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .
