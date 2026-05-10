from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import boto3

# =========================
# CONFIG
# =========================
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================
# APP INIT
# =========================
app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MONGODB
# =========================
client = MongoClient("mongodb://localhost:27017")

db = client["aws_ai"]

users = db["users"]

# =========================
# AWS REGIONS
# =========================
regions = [
    "us-east-1",
    "us-east-2"
]

# =========================
# REGION NAMES
# =========================
region_map = {
    "us-east-1": "N. Virginia 🇺🇸",
    "us-east-2": "Ohio 🇺🇸",
    "us-west-1": "California 🇺🇸",
    "us-west-2": "Oregon 🇺🇸",
    "ap-south-1": "Mumbai 🇮🇳"
}

# =========================
# CLOUDWATCH CLIENT
# =========================
cloudwatch = boto3.client(
    "cloudwatch",
    region_name="us-east-1"
)

# =========================
# GET EC2 INSTANCES
# =========================
def get_ec2_instances():

    all_instances = []

    for region in regions:

        ec2 = boto3.client(
            "ec2",
            region_name=region
        )

        response = ec2.describe_instances()

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                all_instances.append({

                    "InstanceId":
                    instance["InstanceId"],

                    "State":
                    instance["State"]["Name"],

                    "Region":
                    region,

                    "RegionName":
                    region_map.get(region, region)

                })

    return all_instances

# =========================
# GET S3 BUCKETS
# =========================
def get_s3_buckets():

    s3 = boto3.client("s3")

    response = s3.list_buckets()

    buckets = []

    for bucket in response["Buckets"]:
        buckets.append(bucket["Name"])

    return buckets

# =========================
# PASSWORD HASH
# =========================
def hash_password(password: str):

    return pwd_context.hash(password[:72])

# =========================
# VERIFY PASSWORD
# =========================
def verify_password(password, hashed):

    return pwd_context.verify(
        password[:72],
        hashed
    )

# =========================
# CREATE JWT TOKEN
# =========================
def create_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=10)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# =========================
# GET CURRENT USER
# =========================
def get_current_user(token: str = Depends(lambda: None)):

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["username"]

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

# =========================
# HOME
# =========================
@app.get("/")
def home():

    return {
        "message": "AWS AI Backend Running 🚀"
    }

# =========================
# REGISTER
# =========================
@app.post("/register")
def register(data: dict = Body(...)):

    username = data.get("username")
    password = data.get("password")

    if not username or not password:

        raise HTTPException(
            status_code=400,
            detail="Missing fields"
        )

    if users.find_one({
        "username": username
    }):

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    users.insert_one({

        "username": username,

        "password": hash_password(password)

    })

    return {
        "message": "User registered successfully"
    }

# =========================
# LOGIN
# =========================
@app.post("/login")
def login(data: dict = Body(...)):

    username = data.get("username")
    password = data.get("password")

    user = users.find_one({
        "username": username
    })

    if not user:

        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if not verify_password(
        password,
        user["password"]
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    token = create_token({
        "username": username
    })

    return {
        "token": token,
        "username": username
    }

# =========================
# ALL INSTANCES
# =========================
@app.get("/instances")
def instances():

    return get_ec2_instances()

# =========================
# RUNNING INSTANCES
# =========================
@app.get("/running")
def running():

    data = get_ec2_instances()

    running_instances = [

        i for i in data
        if i["State"] == "running"

    ]

    return running_instances

# =========================
# STOPPED INSTANCES
# =========================
@app.get("/stopped")
def stopped():

    data = get_ec2_instances()

    stopped_instances = [

        i for i in data
        if i["State"] == "stopped"

    ]

    return stopped_instances

# =========================
# S3
# =========================
@app.get("/s3")
def s3():

    return get_s3_buckets()

# =========================
# CLOUDWATCH METRICS
# =========================
@app.get("/cloudwatch")
def get_cloudwatch():

    try:

        instances = get_ec2_instances()

        if len(instances) == 0:
            return []

        instance_id = instances[0]["InstanceId"]

        end_time = datetime.utcnow()

        start_time = end_time - timedelta(hours=1)

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"]
        )

        datapoints = response["Datapoints"]

        datapoints.sort(
            key=lambda x: x["Timestamp"]
        )

        result = []

        for point in datapoints:

            result.append({
                "time": point["Timestamp"].strftime("%H:%M"),
                "cpu": round(point["Average"], 2)
            })

        return result

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================
# START INSTANCE
# =========================
@app.post("/start")
def start_instance(data: dict = Body(...)):

    instance_id = data.get("instance_id")

    for region in regions:

        try:

            ec2 = boto3.client(
                "ec2",
                region_name=region
            )

            ec2.start_instances(
                InstanceIds=[instance_id]
            )

            return {
                "message":
                f"✅ Started {instance_id}"
            }

        except:
            pass

    return {
        "message":
        "❌ Instance not found"
    }

# =========================
# STOP INSTANCE
# =========================
@app.post("/stop")
def stop_instance(data: dict = Body(...)):

    instance_id = data.get("instance_id")

    for region in regions:

        try:

            ec2 = boto3.client(
                "ec2",
                region_name=region
            )

            ec2.stop_instances(
                InstanceIds=[instance_id]
            )

            return {
                "message":
                f"🛑 Stopped {instance_id}"
            }

        except:
            pass

    return {
        "message":
        "❌ Instance not found"
    }

# =========================
# REBOOT INSTANCE
# =========================
@app.post("/reboot")
def reboot_instance(data: dict = Body(...)):

    instance_id = data.get("instance_id")

    for region in regions:

        try:

            ec2 = boto3.client(
                "ec2",
                region_name=region
            )

            ec2.reboot_instances(
                InstanceIds=[instance_id]
            )

            return {
                "message":
                f"🔄 Rebooted {instance_id}"
            }

        except:
            pass

    return {
        "message":
        "❌ Instance not found"
    }

# =========================
# AI CHATBOT
# =========================
@app.post("/ai")
def ai_chat(data: dict = Body(...)):

    msg = data.get(
        "message",
        ""
    ).lower()

    instances = get_ec2_instances()

    running = [
        i for i in instances
        if i["State"] == "running"
    ]

    stopped = [
        i for i in instances
        if i["State"] == "stopped"
    ]

    # =========================
    # SHOW INSTANCES
    # =========================
    if (
        "instance" in msg
        or "server" in msg
        or "ec2" in msg
        or "show" in msg
        or "list" in msg
    ):

        text = f"📊 Total EC2 Instances: {len(instances)}\n\n"

        for i in instances:

            text += (
                f"🖥 {i['InstanceId']} | "
                f"{i['State']} | "
                f"{i['RegionName']}\n"
            )

        return {
            "response": text
        }

    # =========================
    # START INSTANCE
    # =========================
    elif "start" in msg:

        for word in msg.split():

            if word.startswith("i-"):

                for region in regions:

                    try:

                        ec2 = boto3.client(
                            "ec2",
                            region_name=region
                        )

                        ec2.start_instances(
                            InstanceIds=[word]
                        )

                        return {
                            "response":
                            f"✅ Instance {word} started"
                        }

                    except:
                        pass

        return {
            "response":
            "❌ Instance ID not found"
        }

    # =========================
    # STOP INSTANCE
    # =========================
    elif "stop" in msg:

        for word in msg.split():

            if word.startswith("i-"):

                for region in regions:

                    try:

                        ec2 = boto3.client(
                            "ec2",
                            region_name=region
                        )

                        ec2.stop_instances(
                            InstanceIds=[word]
                        )

                        return {
                            "response":
                            f"🛑 Instance {word} stopped"
                        }

                    except:
                        pass

        return {
            "response":
            "❌ Instance ID not found"
        }

    # =========================
    # REBOOT INSTANCE
    # =========================
    elif "reboot" in msg:

        for word in msg.split():

            if word.startswith("i-"):

                for region in regions:

                    try:

                        ec2 = boto3.client(
                            "ec2",
                            region_name=region
                        )

                        ec2.reboot_instances(
                            InstanceIds=[word]
                        )

                        return {
                            "response":
                            f"🔄 Instance {word} rebooted"
                        }

                    except:
                        pass

        return {
            "response":
            "❌ Instance ID not found"
        }

    # =========================
    # RUNNING
    # =========================
    elif "running" in msg:

        text = f"🟢 Running Instances: {len(running)}\n\n"

        for i in running:

            text += (
                f"{i['InstanceId']} | "
                f"{i['RegionName']}\n"
            )

        return {
            "response": text
        }

    # =========================
    # STOPPED
    # =========================
    elif "stopped" in msg:

        text = f"🔴 Stopped Instances: {len(stopped)}\n\n"

        for i in stopped:

            text += (
                f"{i['InstanceId']} | "
                f"{i['RegionName']}\n"
            )

        return {
            "response": text
        }

    # =========================
    # COST OPTIMIZATION
    # =========================
    elif (
        "cost" in msg
        or "optimize" in msg
        or "saving" in msg
    ):

        return {
            "response":
            f"💰 You have {len(stopped)} stopped EC2 instances.\n"
            f"Terminate unused resources to reduce AWS cost."
        }

    # =========================
    # S3
    # =========================
    elif (
        "s3" in msg
        or "bucket" in msg
    ):

        buckets = get_s3_buckets()

        return {
            "response":
            f"🪣 Total S3 Buckets: {len(buckets)}\n\n{buckets}"
        }

    # =========================
    # OHIO REGION
    # =========================
    elif "ohio" in msg:

        ohio = [

            i for i in instances
            if i["Region"] == "us-east-2"

        ]

        text = f"🌎 Ohio Region Instances: {len(ohio)}\n\n"

        for i in ohio:

            text += (
                f"{i['InstanceId']} | "
                f"{i['State']}\n"
            )

        return {
            "response": text
        }

    # =========================
    # HELP
    # =========================
    elif "help" in msg:

        return {
            "response":
            "🤖 AWS AI Assistant Commands\n\n"
            "• show instances\n"
            "• running servers\n"
            "• stopped instances\n"
            "• start i-xxxx\n"
            "• stop i-xxxx\n"
            "• reboot i-xxxx\n"
            "• ohio instances\n"
            "• s3 buckets\n"
            "• cost optimization\n"
        }

    # =========================
    # DEFAULT
    # =========================
    else:

        return {
            "response":
            "🤖 Sorry, I didn't understand.\n\n"
            "Try:\n"
            "• show instances\n"
            "• running servers\n"
            "• start i-xxxx\n"
            "• stop i-xxxx\n"
            "• cost optimization\n"
        }