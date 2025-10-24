import boto3
import datetime
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")
cloudwatch = boto3.client("cloudwatch")

def handler(event, context):
    logger.info("=== Checking for idle EC2 instances ===")

    # Find instances with Shutdown: yes
    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Shutdown", "Values": ["yes"]},
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    reservations = response.get("Reservations", [])
    logger.info(f"Found {len(reservations)} reservations with Shutdown:yes")

    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=30)

    for reservation in reservations:
        for instance in reservation.get("Instances", []):
            instance_id = instance["InstanceId"]
            logger.info(f"Checking instance {instance_id}")

            # Get average CPU utilization over last 30 minutes
            metrics = cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=start_time,
                EndTime=now,
                Period=300,  # 5 min period
                Statistics=["Average"]
            )

            datapoints = metrics.get("Datapoints", [])
            logger.debug(f"Raw datapoints for {instance_id}: {datapoints}")

            if not datapoints:
                logger.warning(f"No CPU data for {instance_id}, skipping.")
                continue

            avg_cpu = sum([dp["Average"] for dp in datapoints]) / len(datapoints)
            logger.info(f"Instance {instance_id} average CPU: {avg_cpu:.2f}%")

            if avg_cpu < 5.0:  # threshold for idle
                logger.info(f"Stopping idle instance {instance_id}")
                ec2.stop_instances(InstanceIds=[instance_id])
            else:
                logger.info(f"Instance {instance_id} is active, skipping.")