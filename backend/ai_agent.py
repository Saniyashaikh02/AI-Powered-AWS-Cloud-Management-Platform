import boto3

# =========================
# EC2 CLIENTS
# =========================
ec2_us_east_1 = boto3.client("ec2", region_name="us-east-1")
ec2_us_east_2 = boto3.client("ec2", region_name="us-east-2")

# =========================
# S3 CLIENT
# =========================
s3 = boto3.client("s3")

# =========================
# GET ALL INSTANCES
# =========================
def get_all_instances():

    regions = [
        ("us-east-1", ec2_us_east_1),
        ("us-east-2", ec2_us_east_2)
    ]

    all_instances = []

    for region_name, client in regions:

        response = client.describe_instances()

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:

                state = instance["State"]["Name"]

                all_instances.append({
                    "InstanceId": instance["InstanceId"],
                    "State": state,
                    "Region": region_name
                })

    return all_instances


# =========================
# START INSTANCE
# =========================
def start_instance(instance_id):

    try:

        regions = [
            ec2_us_east_1,
            ec2_us_east_2
        ]

        for client in regions:

            try:
                client.start_instances(
                    InstanceIds=[instance_id]
                )

                return f"✅ Instance {instance_id} started successfully"

            except:
                pass

        return "❌ Instance not found"

    except Exception as e:
        return str(e)


# =========================
# STOP INSTANCE
# =========================
def stop_instance(instance_id):

    try:

        regions = [
            ec2_us_east_1,
            ec2_us_east_2
        ]

        for client in regions:

            try:
                client.stop_instances(
                    InstanceIds=[instance_id]
                )

                return f"🛑 Instance {instance_id} stopped successfully"

            except:
                pass

        return "❌ Instance not found"

    except Exception as e:
        return str(e)


# =========================
# REBOOT INSTANCE
# =========================
def reboot_instance(instance_id):

    try:

        regions = [
            ec2_us_east_1,
            ec2_us_east_2
        ]

        for client in regions:

            try:
                client.reboot_instances(
                    InstanceIds=[instance_id]
                )

                return f"🔄 Instance {instance_id} rebooted"

            except:
                pass

        return "❌ Instance not found"

    except Exception as e:
        return str(e)


# =========================
# LIST S3 BUCKETS
# =========================
def get_s3_buckets():

    response = s3.list_buckets()

    return [bucket["Name"] for bucket in response["Buckets"]]


# =========================
# CREATE S3 BUCKET
# =========================
def create_bucket(bucket_name):

    try:

        s3.create_bucket(
            Bucket=bucket_name
        )

        return f"✅ Bucket {bucket_name} created"

    except Exception as e:
        return str(e)


# =========================
# DELETE S3 BUCKET
# =========================
def delete_bucket(bucket_name):

    try:

        s3.delete_bucket(
            Bucket=bucket_name
        )

        return f"🗑️ Bucket {bucket_name} deleted"

    except Exception as e:
        return str(e)


# =========================
# AI CHAT FUNCTION
# =========================
def ai_chat(message):

    msg = message.lower()

    # =====================
    # SHOW INSTANCES
    # =====================
    if "show instances" in msg or "list instances" in msg:

        instances = get_all_instances()

        if not instances:
            return "❌ No EC2 instances found"

        text = f"📊 Total EC2 Instances: {len(instances)}\n\n"

        for inst in instances:

            text += (
                f"🖥️ {inst['InstanceId']} | "
                f"{inst['State']} | "
                f"{inst['Region']}\n"
            )

        return text

    # =====================
    # START INSTANCE
    # =====================
    elif "start" in msg:

        words = msg.split()

        for word in words:

            if word.startswith("i-"):
                return start_instance(word)

        return "❌ Please provide instance id"

    # =====================
    # STOP INSTANCE
    # =====================
    elif "stop" in msg:

        words = msg.split()

        for word in words:

            if word.startswith("i-"):
                return stop_instance(word)

        return "❌ Please provide instance id"

    # =====================
    # REBOOT INSTANCE
    # =====================
    elif "reboot" in msg:

        words = msg.split()

        for word in words:

            if word.startswith("i-"):
                return reboot_instance(word)

        return "❌ Please provide instance id"

    # =====================
    # LIST BUCKETS
    # =====================
    elif "show buckets" in msg or "list buckets" in msg:

        buckets = get_s3_buckets()

        if not buckets:
            return "❌ No S3 buckets found"

        text = "🪣 S3 Buckets:\n\n"

        for b in buckets:
            text += f"• {b}\n"

        return text

    # =====================
    # CREATE BUCKET
    # =====================
    elif "create bucket" in msg:

        words = msg.split()

        bucket_name = words[-1]

        return create_bucket(bucket_name)

    # =====================
    # DELETE BUCKET
    # =====================
    elif "delete bucket" in msg:

        words = msg.split()

        bucket_name = words[-1]

        return delete_bucket(bucket_name)

    # =====================
    # COST OPTIMIZATION
    # =====================
    elif "cost" in msg or "optimize" in msg:

        instances = get_all_instances()

        stopped = [
            i for i in instances
            if i["State"] == "stopped"
        ]

        if len(stopped) > 0:

            return (
                f"💰 You have {len(stopped)} stopped instances.\n"
                f"Delete unused EBS volumes and stop idle resources "
                f"to reduce AWS cost."
            )

        return "✅ Infrastructure looks optimized"

    # =====================
    # DEFAULT
    # =====================
    return (
        "🤖 I can help with:\n\n"
        "• show instances\n"
        "• start i-xxxx\n"
        "• stop i-xxxx\n"
        "• reboot i-xxxx\n"
        "• show buckets\n"
        "• create bucket test123\n"
        "• delete bucket test123\n"
        "• optimize cost\n"
    )