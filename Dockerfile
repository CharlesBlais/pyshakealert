FROM continuumio/miniconda3

COPY . /opt/pyshakealert

WORKDIR /opt/pyshakealert

RUN python -m pip install --upgrade pip

RUN conda install -y -c conda-forge cartopy

RUN python -m pip install .

CMD /bin/bash
