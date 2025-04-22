FROM python:3.13-alpine AS builder

WORKDIR /build

COPY . .

RUN pip install --upgrade pip build

RUN python -m build --wheel

FROM python:3.13-alpine
LABEL maintainer="Jetsung Chan<i@jetsung.com>"

WORKDIR /app

COPY --from=builder /build/dist /app

RUN pip install /app/*.whl && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["predeldomain"]

CMD ["--help"]
