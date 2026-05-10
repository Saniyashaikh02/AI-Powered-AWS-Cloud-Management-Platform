import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  AreaChart,
  Area
} from "recharts";

import "./CloudWatchCharts.css";

function CloudWatchCharts() {

  // =========================
  // DUMMY CLOUDWATCH DATA
  // =========================

  const cpuData = [
    { time: "1PM", value: 20 },
    { time: "2PM", value: 35 },
    { time: "3PM", value: 50 },
    { time: "4PM", value: 45 },
    { time: "5PM", value: 60 },
    { time: "6PM", value: 40 }
  ];

  const networkData = [
    { time: "1PM", value: 120 },
    { time: "2PM", value: 180 },
    { time: "3PM", value: 160 },
    { time: "4PM", value: 220 },
    { time: "5PM", value: 280 },
    { time: "6PM", value: 240 }
  ];

  const memoryData = [
    { time: "1PM", value: 40 },
    { time: "2PM", value: 50 },
    { time: "3PM", value: 55 },
    { time: "4PM", value: 70 },
    { time: "5PM", value: 65 },
    { time: "6PM", value: 80 }
  ];

  return (
    <div className="charts-section">

      {/* ========================= */}
      {/* CPU CHART */}
      {/* ========================= */}

      <div className="chart-card">

        <div className="chart-header">
          🔥 CPU Utilization
        </div>

        <ResponsiveContainer width="100%" height={260}>

          <LineChart data={cpuData}>

            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

            <XAxis
              dataKey="time"
              stroke="#94a3b8"
            />

            <YAxis stroke="#94a3b8" />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#22c55e"
              strokeWidth={3}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

      {/* ========================= */}
      {/* NETWORK CHART */}
      {/* ========================= */}

      <div className="chart-card">

        <div className="chart-header">
          🌐 Network Traffic
        </div>

        <ResponsiveContainer width="100%" height={260}>

          <AreaChart data={networkData}>

            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

            <XAxis
              dataKey="time"
              stroke="#94a3b8"
            />

            <YAxis stroke="#94a3b8" />

            <Tooltip />

            <Area
              type="monotone"
              dataKey="value"
              stroke="#3b82f6"
              fill="#1d4ed8"
            />

          </AreaChart>

        </ResponsiveContainer>

      </div>

      {/* ========================= */}
      {/* MEMORY CHART */}
      {/* ========================= */}

      <div className="chart-card">

        <div className="chart-header">
          💾 Memory Usage
        </div>

        <ResponsiveContainer width="100%" height={260}>

          <LineChart data={memoryData}>

            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />

            <XAxis
              dataKey="time"
              stroke="#94a3b8"
            />

            <YAxis stroke="#94a3b8" />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#f59e0b"
              strokeWidth={3}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default CloudWatchCharts;