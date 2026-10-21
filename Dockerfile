FROM python:3.12-alpine AS build

WORKDIR /src

COPY tools/ tools/
COPY data/ data/

RUN python tools/build_report.py


FROM build AS test

COPY tests/ tests/

RUN python -m unittest discover -s tests -v


FROM python:3.12-alpine AS final

WORKDIR /velo-alatau

ENV BRANCH="Almaty"
ENV TOP="5"

COPY --from=test /src/out/report.json ./report.json
COPY app/server.py ./server.py

EXPOSE 8080

CMD ["python", "server.py"]
