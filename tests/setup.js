// Jest setup file
// This file runs before all tests

// Set test environment variables
process.env.NODE_ENV = 'test';
process.env.PORT = 3000;
process.env.LOG_LEVEL = 'error'; // Suppress logs during tests

// Mock external services
jest.mock('twilio', () => ({
  Twilio: jest.fn(() => ({
    messages: {
      create: jest.fn(() => Promise.resolve({ sid: 'test_sid' }))
    }
  }))
}));

// Increase timeout for integration tests
jest.setTimeout(10000);
