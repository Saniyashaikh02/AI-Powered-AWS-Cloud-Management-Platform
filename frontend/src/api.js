const API = "http://127.0.0.1:8000";

// =========================
// LOGIN
// =========================
export async function loginUser(username, password) {

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      password
    })
  });

  return await res.json();
}

// =========================
// REGISTER
// =========================
export async function registerUser(username, password) {

  const res = await fetch(`${API}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      password
    })
  });

  return await res.json();
}

// =========================
// GET INSTANCES
// =========================
export async function getInstances() {

  const res = await fetch(`${API}/instances`);

  return await res.json();
}

// =========================
// GET RUNNING
// =========================
export async function getRunning() {

  const res = await fetch(`${API}/running`);

  return await res.json();
}

// =========================
// GET STOPPED
// =========================
export async function getStopped() {

  const res = await fetch(`${API}/stopped`);

  return await res.json();
}

// =========================
// GET S3
// =========================
export async function getS3() {

  const res = await fetch(`${API}/s3`);

  return await res.json();
}

// =========================
// CLOUDWATCH
// =========================
export async function getCloudwatch() {

  const res = await fetch(`${API}/cloudwatch`);

  return await res.json();
}

// =========================
// AI CHAT
// =========================
export async function sendMessage(message) {

  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message
    })
  });

  return await res.json();
}