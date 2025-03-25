# Mawrid Selenium Test Automation

This project contains automated UI tests for the Mawrid application using Selenium WebDriver with Python.

1. Install Python 3.x
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration


## Test Reports

### Run all tests
HTML reports are generated in the `reports` directory after test execution:
```bash
python -m pytest mawrid_admin/tests/ -v --html=report.html
python -m pytest mawrid_user/tests/ -v --html=report.html
python -m pytest mawrid_vendor/tests/ -v --html=report.html
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