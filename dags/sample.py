from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 10, 16),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sample', default_args=default_args, schedule_interval=timedelta(1))

parse_elb_logs = BashOperator(
    task_id='parse_elb_logs',
    bash_command='sleep 1 && echo {p}'.format(p=Variable.get('elb_output')),
    dag=dag)

parse_elb_logs.doc_md = """\
Parses logs from xyz Elastic Load Balancer and writes them as normalized parquet to s3://some-bucket/date=YYYY-MM-DD/
"""

aggregate_stats = BashOperator(
    task_id='aggregate_stats',
    bash_command='sleep 1 && echo {p}'.format(p=Variable.get('stats_output')),
    dag=dag)

aggregate_stats.doc_md = """\
Reads raw events from s3://some-bucket/date=YYYY-MM-DD/, aggregates them and writes them to
the hive data warehouse
"""

copy_hive_to_redshift = BashOperator(
    task_id='copy_hive_to_redshift',
    bash_command='sleep 1 && echo {p}'.format(p=Variable.get('redshift_output')),
    dag=dag)

copy_hive_to_redshift.doc_md = """\
Copies data from hive for the execution date to Amazon Redshift for downstream consumers
"""

insert_data_to_cache = BashOperator(
    task_id='insert_data_to_cache',
    bash_command='sleep 1 && echo {p}'.format(p=Variable.get('cache_output')),
    dag=dag)

insert_data_to_cache.doc_md = """\
Copies aggregate data from Redshift to Postgres for analytics dashboard
"""

insert_data_to_cache.set_upstream(copy_hive_to_redshift)
copy_hive_to_redshift.set_upstream(aggregate_stats)
aggregate_stats.set_upstream(parse_elb_logs)
