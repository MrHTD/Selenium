# Mawrid Selenium Test Automation

This project contains automated UI tests for the Mawrid application using Selenium WebDriver with Python.

1. Install Python 3.x
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Update `config/config.py` with your test environment settings:
   - Base URL
   - Browser settings
   - Test credentials
   - Timeouts

## Running Tests

### Run all tests
```bash
pytest src/tests
```

### Run specific test file
```bash
pytest src/tests/test_signup.py
```

### Run tests with specific marker
```bash
pytest -m smoke
```

### Run tests in parallel
```bash
pytest -n auto
```

## Test Reports

HTML reports are generated in the `reports` directory after test execution:
```bash
pytest --html=reports/report.html
```

## Best Practices

1. Follow Page Object Model pattern
2. Use explicit waits instead of implicit waits
3. Keep tests independent
4. Use meaningful test names
5. Add proper assertions
6. Handle exceptions appropriately

## Contributing

1. Create a new branch for your changes
2. Follow the existing code structure
3. Add appropriate comments
4. Update documentation as needed
5. Create a pull request

## Common Issues

- WebDriver compatibility issues
- Element not found exceptions
- Timing issues
- Browser differences

## Contact

For questions or issues, please contact [Your Name/Team]