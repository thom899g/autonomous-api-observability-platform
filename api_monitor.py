from fastapi import FastAPI
from statsd import StatsClient

app = FastAPI()

# Initialize StatsD client
STATSD_HOST = 'localhost'
STATSD_PORT = 8125
statsd = StatsClient(STATSD_HOST, STATSD_PORT)

@app.get('/metrics')
async def metrics():
    try:
        # Collect current request latencies and error rates
        data = collect_api_metrics()
        return {'status': 'success', 'data': data}
    except Exception as e:
        statsd.incr('api_monitor.error.count')
        statsd.timing('api_monitor.error.latency', 500)
        raise HTTPException(status_code=500, detail=str(e))