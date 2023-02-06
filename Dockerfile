FROM python:3.8-slim-buster
WORKDIR .
RUN pip3 install numpy
RUN pip3 install Pillow
RUN pip3 install tkinter
RUN pip3 install matplotlib
RUN pip3 install tkhtmlview
COPY . .
CMD [ "python3", "DiceRoller.py"]