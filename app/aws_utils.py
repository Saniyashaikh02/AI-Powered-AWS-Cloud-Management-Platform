import boto3

# 🌍 Multi-region support
REGIONS = ["us-east-1", "us-east-2", "ap-south-1"]


# ===== EC2 (multi-region) =====
def list_ec2_instances():
    all_instances = []

    for region in REGIONS:
        ec2 = boto3.client('ec2', region_name=region)

        try:
            response = ec2.describe_instances()

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    all_instances.append({
                        "InstanceId": instance['InstanceId'],
                        "State": instance['State']['Name'],
                        "Region": region
                    })

        except Exception as e:
            print(f"Error in {region}: {e}")

    return all_instances


# ===== STOPPED =====
def find_stopped_instances():
    instances = list_ec2_instances()
    return [i for i in instances if i["State"] == "stopped"]


# ===== S3 =====
def list_s3_buckets():
    s3 = boto3.client('s3')

    response = s3.list_buckets()

    return [bucket['Name'] for bucket in response['Buckets']]


# ===== COST =====
def estimate_ec2_cost(stopped_instances):
    cost_per_instance = 5
    return len(stopped_instances) * cost_per_instance


# ===== SMART RECOMMENDATIONS =====
def generate_recommendations(instances, stopped_instances):
    recommendations = []

    if stopped_instances:
        for inst in stopped_instances:
            recommendations.append(
                f"⚠️ Instance {inst['InstanceId']} in {inst['Region']} is stopped.\n"
                f"👉 Consider terminating it or taking a snapshot to save cost."
            )

    if not recommendations:
        recommendations.append("✅ Your infrastructure looks optimized.")

    return recommendations