# AGENT.md - Super Resolution Flask App

## Project Overview
Flask web app for AI-powered image super-resolution using Hugging Face Real-ESRGAN models. Chinese language project with responsive web interface.

## Build/Run Commands
- `python app.py` - Start development server on port 5001
- `./run.sh` - Full startup script with environment setup and port cleanup
- `gunicorn -w 1 -b 0.0.0.0:$PORT app:app` - Production server (Render deployment)

## Test Commands
- `cd test && ./run_tests.sh` - Run all tests
- `cd test && python3 test_api_connection.py` - Test HF API connection only
- `cd test && python3 test_hf_api.py` - Test HF API functionality
- `cd test && python3 test_real_esrgan.py` - Test Real-ESRGAN model
- `cd test && python3 test_stable_diffusion_upscaler.py` - Test SD upscaler

## Architecture
- Flask backend with `/upscale`, `/health`, `/info`, `/test-api` endpoints
- Frontend: HTML/CSS/JS in templates/static directories
- AI model: Hugging Face Real-ESRGAN via Inference API
- Environment: Requires HF_API_TOKEN, optional PORT (default 5001)

## Code Conventions
- Python: PEP 8 style, 4-space indentation
- Logging: Use `logging` module with INFO level
- Error handling: Try/catch with detailed logging, return JSON error responses
- API responses: Always return JSON with error/success status
- File uploads: 5MB limit validation, base64 encoding for responses
