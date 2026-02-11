const request = require('supertest');

describe('Health Check', () => {
  let app;

  beforeAll(() => {
    // Mock environment for testing
    process.env.NODE_ENV = 'test';
    process.env.PORT = 3000;
    
    // Import app after setting environment
    app = require('../src/server');
  });

  it('should return 200 status on health endpoint', async () => {
    const response = await request(app).get('/health');
    
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('status');
    expect(response.body.status).toBe('healthy');
  });

  it('should return application info on root endpoint', async () => {
    const response = await request(app).get('/');
    
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('name');
    expect(response.body).toHaveProperty('status');
  });

  it('should return API status', async () => {
    const response = await request(app).get('/api/status');
    
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('api');
    expect(response.body).toHaveProperty('features');
  });

  it('should return 404 for unknown routes', async () => {
    const response = await request(app).get('/unknown-route');
    
    expect(response.status).toBe(404);
    expect(response.body).toHaveProperty('error');
  });
});
