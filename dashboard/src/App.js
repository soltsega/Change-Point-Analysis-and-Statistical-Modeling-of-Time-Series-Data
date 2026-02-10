import React, { useState, useEffect } from 'react';
import { Layout, Row, Col, Card, DatePicker, Button, Typography, Space, Statistic, Alert, Spin } from 'antd';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, ScatterChart, Scatter } from 'recharts';
import { ReloadOutlined, CalendarOutlined, BarChartOutlined } from '@ant-design/icons';
import axios from 'axios';
import moment from 'moment';
import './App.css';

const { Header, Content } = Layout;
const { RangePicker } = DatePicker;
const { Title, Text } = Typography;

function App() {
  const [data, setData] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState([
    moment('2020-01-01'),
    moment('2026-02-06')
  ]);
  const [error, setError] = useState(null);

  // Load initial data
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load all data in parallel
      const [dataRes, eventsRes, changePointRes, analysisRes] = await Promise.all([
        axios.get('/api/data'),
        axios.get('/api/events'),
        axios.get('/api/change-point'),
        axios.get('/api/analysis')
      ]);

      setData(dataRes.data);
      setEvents(eventsRes.data.events || []);
      setChangePoint(changePointRes.data);
      setAnalysis(analysisRes.data);
      
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (dates) => {
    if (dates && dates[0] && dates[1]) {
      setDateRange(dates);
      loadFilteredData(dates[0], dates[1]);
    }
  };

  const loadFilteredData = async (startDate, endDate) => {
    try {
      const start = startDate.format('YYYY-MM-DD');
      const end = endDate.format('YYYY-MM-DD');
      
      const [dataRes, eventsRes] = await Promise.all([
        axios.get(`/api/data?start_date=${start}&end_date=${end}`),
        axios.get(`/api/events?start_date=${start}&end_date=${end}`)
      ]);

      setData(dataRes.data);
      setEvents(eventsRes.data.events || []);
      
    } catch (err) {
      console.error('Error loading filtered data:', err);
      setError('Failed to load filtered data.');
    }
  };

  // Prepare chart data
  const chartData = data.dates ? data.dates.map((date, index) => ({
    date: moment(date).format('YYYY-MM-DD'),
    price: data.prices[index],
    logReturn: data.log_returns[index],
    rollingMean: analysis?.rolling_mean[index] || 0,
    rollingStd: analysis?.rolling_std[index] || 0,
    rollingVolatility: analysis?.rolling_volatility[index] || 0,
    highVolatility: analysis?.high_volatility[index] || false
  })) : [];

  // Prepare events for chart
  const eventsForChart = events.map(event => ({
    date: moment(event.date).format('YYYY-MM-DD'),
    event: event.event,
    impact: event.impact,
    price: data.prices[data.dates?.indexOf(event.date)] || 0
  }));

  if (loading) {
    return (
      <Layout className="app-layout">
        <Content style={{ padding: '50px', textAlign: 'center' }}>
          <Spin size="large" />
          <Title level={3} style={{ marginTop: 20 }}>Loading Dashboard...</Title>
        </Content>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout className="app-layout">
        <Content style={{ padding: '50px' }}>
          <Alert
            message="Error"
            description={error}
            type="error"
            showIcon
            action={
              <Button type="primary" onClick={loadData}>
                Retry
              </Button>
            }
          />
        </Content>
      </Layout>
    );
  }

  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <div className="header-content">
          <Title level={3} style={{ color: 'white', margin: 0 }}>
            🚀 Brent Oil Price Change Point Analysis
          </Title>
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            onClick={loadData}
            loading={loading}
          >
            Refresh Data
          </Button>
        </div>
      </Header>
      
      <Content style={{ padding: '24px' }}>
        {/* Controls */}
        <Card className="controls-card" title="Dashboard Controls">
          <Row gutter={[16, 16]} align="middle">
            <Col>
              <Space>
                <CalendarOutlined />
                <Text strong>Date Range:</Text>
              </Space>
            </Col>
            <Col>
              <RangePicker
                value={dateRange}
                onChange={handleDateRangeChange}
                format="YYYY-MM-DD"
                size="large"
              />
            </Col>
            <Col>
              <Space>
                <BarChartOutlined />
                <Text strong>Window Size:</Text>
              </Space>
            </Col>
          </Row>
        </Card>

        {/* Summary Statistics */}
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Observations"
                value={analysis?.summary_stats?.total_observations || 0}
                prefix="📊"
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Price Range"
                value={`$${(analysis?.summary_stats?.price_stats?.min || 0).toFixed(2)} - $${(analysis?.summary_stats?.price_stats?.max || 0).toFixed(2)}`}
                prefix="💰"
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Mean Return"
                value={(analysis?.summary_stats?.returns_stats?.mean || 0).toFixed(6)}
                prefix="📈"
                suffix="%"
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Volatility"
                value={(analysis?.summary_stats?.returns_stats?.std || 0).toFixed(4)}
                prefix="📊"
              />
            </Card>
          </Col>
        </Row>

        {/* Change Point Analysis */}
        {changePoint && (
          <Card className="change-point-card" title="🎯 Change Point Analysis" style={{ marginBottom: 24 }}>
            <Row gutter={[16, 16]}>
              <Col xs={24} sm={12} md={8}>
                <Statistic
                  title="Change Point Date"
                  value={changePoint.date}
                  prefix="📅"
                />
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Statistic
                  title="Mean Shift"
                  value={changePoint.mean_shift}
                  prefix="📈"
                  precision={6}
                />
              </Col>
              <Col xs={24} sm={12} md={8}>
                <Statistic
                  title="Volatility Change"
                  value={changePoint.volatility_change}
                  prefix="📊"
                  suffix="%"
                  precision={1}
                />
              </Col>
            </Row>
          </Card>
        )}

        {/* Main Price Chart */}
        <Card title="📈 Price Series with Change Point" style={{ marginBottom: 24 }}>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => moment(value).format('MMM DD')}
              />
              <YAxis />
              <Tooltip 
                labelFormatter={(value) => moment(value).format('YYYY-MM-DD')}
                formatter={(value, name) => [
                  name === 'price' ? `$${value.toFixed(2)}` : value.toFixed(4),
                  name === 'price' ? 'Price' : name
                ]}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#1890ff" 
                strokeWidth={2}
                dot={false}
                name="Price"
              />
              {changePoint && (
                <ReferenceLine 
                  x={changePoint.date} 
                  stroke="#ff4d4f" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  label="Change Point"
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Volatility Analysis */}
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={24} lg={12}>
            <Card title="📊 Volatility Analysis">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={(value) => moment(value).format('MMM DD')}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(value) => moment(value).format('YYYY-MM-DD')}
                    formatter={(value) => [value.toFixed(4), 'Volatility']}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="rollingVolatility" 
                    stroke="#52c41a" 
                    strokeWidth={2}
                    dot={false}
                    name="Rolling Volatility"
                  />
                  {analysis?.volatility_threshold && (
                    <ReferenceLine 
                      y={analysis.volatility_threshold} 
                      stroke="#ff4d4f" 
                      strokeWidth={1}
                      strokeDasharray="3 3"
                      label="90th Percentile"
                    />
                  )}
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </Col>
          
          <Col xs={24} lg={12}>
            <Card title="🎯 Events Timeline">
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart data={eventsForChart}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    type="category"
                    tickFormatter={(value) => moment(value).format('MMM DD')}
                  />
                  <YAxis 
                    dataKey="price" 
                    type="number"
                    domain={['dataMin - 5', 'dataMax + 5']}
                  />
                  <Tooltip 
                    labelFormatter={(value) => moment(value).format('YYYY-MM-DD')}
                    formatter={(value, name) => [
                      value,
                      name === 'price' ? 'Price' : name
                    ]}
                  />
                  <Scatter 
                    dataKey="price" 
                    fill="#ff4d4f"
                    shape="circle"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </Card>
          </Col>
        </Row>

        {/* Events List */}
        <Card title="📋 Major Events" style={{ marginBottom: 24 }}>
          <div className="events-list">
            {events.map((event, index) => (
              <div key={index} className="event-item">
                <Row gutter={[16, 8]} align="middle">
                  <Col xs={24} sm={6}>
                    <Text strong>{moment(event.date).format('YYYY-MM-DD')}</Text>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Text>{event.event}</Text>
                  </Col>
                  <Col xs={24} sm={6}>
                    <Text className={`impact-badge impact-${event.impact.toLowerCase()}`}>
                      {event.impact} Impact
                    </Text>
                  </Col>
                </Row>
              </div>
            ))}
          </div>
        </Card>
      </Content>
    </Layout>
  );
}

export default App;
