"""
Rate limiting module for Faculty API.

This module provides rate limiting functionality using Redis to prevent API abuse.
"""

import os
import asyncio
from typing import Callable
import logging
from fastapi import FastAPI, Request, Response
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Different rate limits (requests per minute)
RATE_LIMIT_PUBLIC = 30  # 30 requests per minute for public endpoints
RATE_LIMIT_USER = 100   # 100 requests per minute for authenticated users
RATE_LIMIT_ADMIN = 300  # 300 requests per minute for admin users

# Initialize Redis connection
async def setup_limiter(app: FastAPI):
    """Initialize Redis connection for rate limiting."""
    try:
        redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
        if REDIS_PASSWORD:
            redis_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
            
        # Connect to Redis
        redis_client = redis.from_url(redis_url)
        
        # Check connection
        await redis_client.ping()
        logger.info("Successfully connected to Redis for rate limiting")
        
        # Initialize FastAPILimiter
        await FastAPILimiter.init(redis_client)
        
        # Log successful initialization
        logger.info("Rate limiter initialized successfully")
        
        # Set up shutdown handler
        @app.on_event("shutdown")
        async def shutdown_limiter():
            """Close Redis connection on shutdown."""
            await redis_client.close()
            logger.info("Rate limiter Redis connection closed")
            
    except Exception as e:
        logger.error(f"Failed to initialize rate limiter: {e}")
        logger.warning("API will run without rate limiting - not recommended for production!")

# Rate limiter dependencies for different user roles
def rate_limit_public() -> Callable:
    """Rate limiter for public (unauthenticated) endpoints."""
    return RateLimiter(times=RATE_LIMIT_PUBLIC, seconds=60)

def rate_limit_user() -> Callable:
    """Rate limiter for authenticated user endpoints."""
    return RateLimiter(times=RATE_LIMIT_USER, seconds=60)

def rate_limit_admin() -> Callable:
    """Rate limiter for admin endpoints."""
    return RateLimiter(times=RATE_LIMIT_ADMIN, seconds=60)

# Function to get appropriate rate limiter based on user role
def get_rate_limiter_by_role(role: str = None) -> Callable:
    """Get appropriate rate limiter based on user role."""
    if role == "admin":
        return rate_limit_admin()
    elif role:  # Any authenticated user
        return rate_limit_user()
    else:  # Public/unauthenticated
        return rate_limit_public()

# Middleware for adding rate limit headers
@asyncio.coroutine
async def add_rate_limit_headers(request: Request, response: Response):
    """Add rate limit headers to responses."""
    # These headers would normally be added by FastAPILimiter
    # This is a placeholder to demonstrate how it would work
    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_PUBLIC)
    response.headers["X-RateLimit-Remaining"] = "Unknown"  # Would be calculated
    response.headers["X-RateLimit-Reset"] = "Unknown"  # Would be calculated
