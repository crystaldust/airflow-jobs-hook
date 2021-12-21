FROM alpine/git:v2.32.0
RUN git clone https://github.com/crystaldust/airflow-jobs-hook.git /airflow-jobs-hook


FROM python:3.8-alpine
COPY --from=0 /airflow-jobs-hook /airflow-jobs-hook
WORKDIR /airflow-jobs-hook 
RUN pip install -r ./requirements.txt

CMD ["uvicorn main:app"]

