import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import CloudWatchCharts from "../components/CloudWatchCharts";

import {
  getInstances,
  getS3
} from "../api";

import "./Dashboard.css";

function Dashboard({ setPage }) {

  const [instances, setInstances] = useState([]);
  const [running, setRunning] = useState([]);
  const [stopped, setStopped] = useState([]);
  const [buckets, setBuckets] = useState([]);

  // =========================
  // 🌍 REGION MAPPING
  // =========================

  const regionMap = {
    "us-east-1": "N. Virginia 🇺🇸",
    "us-east-2": "Ohio 🇺🇸",
    "us-west-1": "N. California 🇺🇸",
    "us-west-2": "Oregon 🇺🇸",
    "ap-south-1": "Mumbai 🇮🇳",
    "ap-northeast-1": "Tokyo 🇯🇵",
    "ap-southeast-1": "Singapore 🇸🇬"
  };

  // =========================
  // LOAD DATA
  // =========================

  useEffect(() => {

    async function loadData() {

      try {

        const inst = await getInstances();
        const s3 = await getS3();

        setInstances(inst || []);
        setBuckets(s3 || []);

        // =========================
        // FILTER RUNNING / STOPPED
        // =========================

        const runningInstances = (inst || []).filter(
          (i) => i.State === "running"
        );

        const stoppedInstances = (inst || []).filter(
          (i) => i.State === "stopped"
        );

        setRunning(runningInstances);
        setStopped(stoppedInstances);

      } catch (err) {

        console.error("Error loading data:", err);

      }
    }

    loadData();

  }, []);

  // =========================
  // LOGOUT
  // =========================

  const logout = () => {

    localStorage.removeItem("token");

    setPage("login");
  };

  return (

    <div className="layout">

      {/* ========================= */}
      {/* SIDEBAR */}
      {/* ========================= */}

      <Sidebar setPage={setPage} />

      {/* ========================= */}
      {/* MAIN CONTENT */}
      {/* ========================= */}

      <div className="content">

        {/* ========================= */}
        {/* NAVBAR */}
        {/* ========================= */}

        <Navbar onLogout={logout} />

        {/* ========================= */}
        {/* HEADER */}
        {/* ========================= */}

        <h1>📊 Dashboard Overview</h1>

        {/* ========================= */}
        {/* STATS CARDS */}
        {/* ========================= */}

        <div className="cards">

          {/* TOTAL */}

          <div className="card">

            <h3>Total Instances</h3>

            <p>{instances.length}</p>

          </div>

          {/* RUNNING */}

          <div className="card green">

            <h3>Running</h3>

            <p>{running.length}</p>

          </div>

          {/* STOPPED */}

          <div className="card red">

            <h3>Stopped</h3>

            <p>{stopped.length}</p>

          </div>

          {/* S3 */}

          <div className="card">

            <h3>S3 Buckets</h3>

            <p>{buckets.length}</p>

          </div>

        </div>

        {/* ========================= */}
        {/* ALERT BOX */}
        {/* ========================= */}

        {stopped.length > 0 && (

          <div className="alert">

            ⚠️ {stopped.length} instance(s) stopped → possible cost waste

          </div>

        )}

        {/* ========================= */}
        {/* EC2 TABLE */}
        {/* ========================= */}

        <div className="table-box">

          <table>

            <thead>

              <tr>

                <th>Instance ID</th>

                <th>Status</th>

                <th>Region</th>

              </tr>

            </thead>

            <tbody>

              {instances.map((inst, index) => (

                <tr key={index}>

                  {/* INSTANCE ID */}

                  <td>

                    {inst.InstanceId}

                  </td>

                  {/* STATUS */}

                  <td>

                    <span
                      className={
                        inst.State === "running"
                          ? "badge green"
                          : "badge red"
                      }
                    >

                      {inst.State}

                    </span>

                  </td>

                  {/* REGION */}

                  <td>

                    {inst.Region} (

                    {regionMap[inst.Region] || "Unknown"}

                    )

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        {/* ========================= */}
        {/* S3 SECTION */}
        {/* ========================= */}

        <div className="s3-box">

          <h3>🪣 S3 Buckets</h3>

          {buckets.length === 0 ? (

            <p>No buckets found</p>

          ) : (

            <ul>

              {buckets.map((b, i) => (

                <li key={i}>

                  {b}

                </li>

              ))}

            </ul>

          )}

        </div>

        {/* ========================= */}
        {/* CLOUDWATCH CHARTS */}
        {/* ========================= */}

        <CloudWatchCharts />

      </div>

    </div>
  );
}

export default Dashboard;