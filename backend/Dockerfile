FROM python:3.12.5-slim

WORKDIR /build

COPY pyproject.toml ./



RUN which python

# RUN python -m venv linux
# RUN ls -l linux/bin/*
# RUN . ./linux/bin/activate

RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple/
# RUN pip install uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple/
# RUN poetry shell
RUN poetry config virtualenvs.create false
RUN poetry install

WORKDIR /app
# COPY . .

# CMD [ "python" ]
