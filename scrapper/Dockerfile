FROM public.ecr.aws/lambda/python:3.11

RUN pip install pytest flake8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY test_app.py ${LAMBDA_TASK_ROOT}


RUN cd ${LAMBDA_TASK_ROOT} \
    && flake8 *.py \
    && pytest .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
