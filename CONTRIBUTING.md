# Contributing to Biz-Bot

Thank you for your interest in contributing to Biz-Bot! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Biz-Bot.git
   cd Biz-Bot
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/brandonlacoste9-tech/Biz-Bot.git
   ```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Git

### Setup

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Start development environment**:
   ```bash
   make dev
   # or
   docker-compose up -d
   ```

3. **Install dependencies** (for local development):
   ```bash
   npm install
   ```

4. **Verify setup**:
   ```bash
   curl http://localhost:3000/health
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-feature`
- `bugfix/fix-issue-123`
- `docs/update-readme`
- `refactor/improve-performance`

### Workflow

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   npm test
   npm run lint
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Guidelines

Follow the Conventional Commits specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add WhatsApp message queuing
fix: resolve database connection timeout
docs: update deployment guide
refactor: improve error handling in webhook
```

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run specific test file
npm test -- path/to/test.js

# Run with coverage
npm test -- --coverage
```

### Writing Tests

- Place test files next to the code they test or in `__tests__` directories
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies

Example:
```javascript
describe('Health Endpoint', () => {
  it('should return 200 status and healthy message', async () => {
    // Arrange
    const response = await request(app).get('/health');
    
    // Assert
    expect(response.status).toBe(200);
    expect(response.body.status).toBe('healthy');
  });
});
```

## Submitting Changes

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**:
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
```

## Style Guidelines

### JavaScript/Node.js

- Use ES6+ features
- Use `const` and `let`, not `var`
- Use arrow functions where appropriate
- Use template literals for string interpolation
- Use async/await instead of callbacks
- Add JSDoc comments for functions

Example:
```javascript
/**
 * Processes incoming WhatsApp message
 * @param {Object} message - The message object
 * @param {string} message.from - Sender phone number
 * @param {string} message.body - Message content
 * @returns {Promise<Object>} Processed response
 */
async function processMessage({ from, body }) {
  // Implementation
}
```

### Code Organization

- Keep functions small and focused
- Use meaningful variable names
- Separate concerns (MVC pattern)
- Avoid deep nesting (max 3 levels)

### File Structure

```
src/
├── controllers/   # Route handlers
├── models/        # Database models
├── services/      # Business logic
├── utils/         # Utility functions
├── middleware/    # Express middleware
└── config/        # Configuration files
```

### Error Handling

Always handle errors gracefully:

```javascript
try {
  const result = await someAsyncOperation();
  return result;
} catch (error) {
  logger.error('Operation failed', { error: error.message });
  throw new CustomError('Operation failed', 500);
}
```

### Environment Variables

- Never commit `.env` files
- Document all environment variables in `.env.example`
- Use descriptive variable names
- Provide default values where appropriate

### Docker

- Keep Dockerfile simple and efficient
- Use multi-stage builds
- Minimize layer count
- Don't run as root in production

### Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add inline comments for complex logic
- Write clear commit messages

## Review Process

### What We Look For

- **Code Quality**: Clean, readable, maintainable code
- **Testing**: Adequate test coverage
- **Documentation**: Updated docs where needed
- **Performance**: No significant performance degradation
- **Security**: No security vulnerabilities introduced

### Review Timeline

- Small PRs: 1-2 days
- Medium PRs: 3-5 days
- Large PRs: 1+ weeks

### Addressing Feedback

- Respond to all review comments
- Make requested changes promptly
- Ask questions if you need clarification
- Re-request review after making changes

## Questions?

- Open an issue for general questions
- Use discussions for feature proposals
- Tag maintainers for urgent issues

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to Biz-Bot! 🎉
