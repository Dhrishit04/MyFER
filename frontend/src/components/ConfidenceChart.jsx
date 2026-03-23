import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const ConfidenceChart = ({ scores }) => {
  // Convert dict to array of objects and sort by confidence descending
  const data = Object.entries(scores)
    .map(([name, value]) => ({ name, value: value * 100 }))
    .sort((a, b) => b.value - a.value);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-dark-bg border border-dark-border p-3 rounded shadow-lg text-sm">
          <p className="text-gray-200 font-medium">{payload[0].payload.name}</p>
          <p className="text-dark-accent">{payload[0].value.toFixed(2)}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-80 pt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <XAxis type="number" hide domain={[0, 100]} />
          <YAxis 
            dataKey="name" 
            type="category" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#9ca3af', fontSize: 13 }}
          />
          <Tooltip cursor={{ fill: '#ffffff0a' }} content={<CustomTooltip />} />
          <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20}>
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={index === 0 ? '#00D1FF' : '#2A2E39'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConfidenceChart;
